"""后台错误日志管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import BError
from myapp.serializers import BErrorSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """错误日志列表接口"""
    try:
        # 获取查询参数
        error_type = request.GET.get('error_type', '')
        handle_status = request.GET.get('handle_status', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 基础查询集
        errors = BError.objects.all()
        
        # 错误类型筛选
        if error_type:
            errors = errors.filter(error_type__contains=error_type)
        
        # 处理状态筛选
        if handle_status:
            errors = errors.filter(handle_status=handle_status)
        
        # 时间范围筛选
        if start_date:
            errors = errors.filter(error_time__gte=start_date)
        if end_date:
            errors = errors.filter(error_time__lte=end_date)
        
        # 关键词搜索（错误信息、用户信息）
        if keyword:
            errors = errors.filter(
                Q(error_message__contains=keyword) |
                Q(user_id__user_name__contains=keyword) |
                Q(user_id__user_student_id__contains=keyword)
            )
        
        # 总数
        total = errors.count()
        
        # 分页（按错误时间倒序）
        start = (page - 1) * page_size
        end = start + page_size
        errors = errors.order_by('-error_time')[start:end]
        
        # 序列化
        serializer = BErrorSerializer(errors, many=True)
        
        return APIResponse(code=0, msg='查询成功', data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update_status(request):
    """更新错误处理状态"""
    try:
        error_id = request.data.get('b_error_id')
        handle_status = request.data.get('handle_status')
        handle_detail = request.data.get('handle_detail', '')
        
        if not error_id or not handle_status:
            return APIResponse(code=1, msg='错误ID和处理状态不能为空')
        
        error = BError.objects.get(b_error_id=error_id)
        
        # 更新处理状态
        error.handle_status = handle_status
        error.handle_detail = handle_detail
        
        # 如果标记为已处理，记录处理时间
        from django.utils import timezone
        if handle_status in ['已处理', '已修复', '已忽略']:
            error.handle_time = timezone.now()
        
        error.save()
        
        serializer = BErrorSerializer(error)
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
        
    except BError.DoesNotExist:
        return APIResponse(code=1, msg='错误日志不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'更新失败: {str(e)}')