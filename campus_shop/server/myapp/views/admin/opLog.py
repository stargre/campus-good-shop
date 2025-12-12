"""后台操作日志管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import BOp
from myapp.serializers import BOpSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """操作日志列表接口"""
    try:
        # 获取查询参数
        op_type = request.GET.get('op_type', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 基础查询集
        op_logs = BOp.objects.all()
        
        # 操作类型筛选
        if op_type:
            op_logs = op_logs.filter(op_type=op_type)
        
        # 时间范围筛选
        if start_date:
            op_logs = op_logs.filter(op_time__gte=start_date)
        if end_date:
            op_logs = op_logs.filter(op_time__lte=end_date)
        
        # 关键词搜索（用户信息、操作对象、详情）
        if keyword:
            op_logs = op_logs.filter(
                Q(user_id__user_name__contains=keyword) |
                Q(user_id__user_student_id__contains=keyword) |
                Q(op_object__contains=keyword) |
                Q(op_detail__contains=keyword)
            )
        
        # 总数
        total = op_logs.count()
        
        # 分页（按操作时间倒序）
        start = (page - 1) * page_size
        end = start + page_size
        op_logs = op_logs.order_by('-op_time')[start:end]
        
        # 序列化
        serializer = BOpSerializer(op_logs, many=True)
        
        return APIResponse(code=0, msg='查询成功', data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')