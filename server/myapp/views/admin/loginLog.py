"""后台登录日志管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import BLogin
from myapp.serializers import BLoginSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """登录日志列表接口"""
    try:
        # 获取查询参数
        login_status = request.GET.get('login_status', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 基础查询集
        login_logs = BLogin.objects.all()
        
        # 登录状态筛选
        if login_status != '':
            login_logs = login_logs.filter(login_status=(login_status == 'true'))
        
        # 时间范围筛选
        if start_date:
            login_logs = login_logs.filter(login_time__gte=start_date)
        if end_date:
            login_logs = login_logs.filter(login_time__lte=end_date)
        
        # 关键词搜索（用户信息、IP、设备）
        if keyword:
            login_logs = login_logs.filter(
                Q(user_id__user_name__contains=keyword) |
                Q(user_id__user_student_id__contains=keyword) |
                Q(ip_address__contains=keyword) |
                Q(login_device__contains=keyword)
            )
        
        # 总数
        total = login_logs.count()
        
        # 分页（按登录时间倒序）
        start = (page - 1) * page_size
        end = start + page_size
        login_logs = login_logs.order_by('-login_time')[start:end]
        
        # 序列化
        serializer = BLoginSerializer(login_logs, many=True)
        
        return APIResponse(code=0, msg='查询成功', data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')