"""后台浏览记录管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.models import Record, UserInfo, Product
from myapp.serializers import RecordSerializer
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Record, UserInfo, Product
from myapp.serializers import RecordSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """浏览记录列表接口"""
    try:
        # 获取查询参数
        user_id = request.GET.get('user_id', '')
        product_id = request.GET.get('product_id', '')
        keyword = request.GET.get('keyword', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 基础查询集
        records = Record.objects.all()
        
        # 用户筛选
        if user_id:
            records = records.filter(user_id=user_id)
        
        # 商品筛选
        if product_id:
            records = records.filter(product_id=product_id)
        
        # 关键词搜索（用户姓名、学号、商品标题）
        if keyword:
            records = records.filter(
                Q(user_id__user_name__contains=keyword) |
                Q(user_id__user_student_id__contains=keyword) |
                Q(product_id__product_title__contains=keyword)
            )
        
        # 时间范围筛选
        if start_date:
            records = records.filter(create_time__gte=start_date)
        if end_date:
            records = records.filter(create_time__lte=end_date)
        
        # 总数
        total = records.count()
        
        # 分页（按浏览时间倒序）
        start = (page - 1) * page_size
        end = start + page_size
        records = records.order_by('-create_time')[start:end]
        
        # 序列化
        serializer = RecordSerializer(records, many=True)
        
        return APIResponse(code=0, msg='查询成功', data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_page': (total + page_size - 1) // page_size
        })
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除浏览记录接口"""
    try:
        record_id = request.data.get('record_id')
        if not record_id:
            return APIResponse(code=1, msg='记录ID不能为空')
        
        record = Record.objects.get(record_id=record_id)
        record.delete()
        
        return APIResponse(code=0, msg='删除成功')
    except Record.DoesNotExist:
        return APIResponse(code=1, msg='记录不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def deleteAll(request):
    """清空所有浏览记录接口"""
    try:
        # 可以添加权限验证，只有超级管理员可以清空所有记录
        user_id = request.data.get('user_id', '')
        
        if user_id:
            # 清空指定用户的所有浏览记录
            Record.objects.filter(user_id=user_id).delete()
            return APIResponse(code=0, msg=f'已清空用户{user_id}的所有浏览记录')
        else:
            # 清空所有浏览记录（谨慎操作）
            # 可以添加确认机制
            confirm = request.data.get('confirm', '')
            if confirm != 'YES_DELETE_ALL':
                return APIResponse(code=1, msg='请确认操作，需要传递confirm=YES_DELETE_ALL参数')
            
            Record.objects.all().delete()
            return APIResponse(code=0, msg='已清空所有浏览记录')
            
    except Exception as e:
        return APIResponse(code=1, msg=f'清空失败: {str(e)}')