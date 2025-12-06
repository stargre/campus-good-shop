"""
前台浏览记录视图模块
提供用户浏览记录相关接口
"""
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from myapp.auth.authentication import TokenAuthtication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from myapp.handler import APIResponse
from myapp.models import Record, Product
from myapp.serializers import RecordSerializer


@api_view(['GET'])
def create(request):
    """
    创建浏览记录接口
    查询参数: product_id（商品ID）
    Returns:
        APIResponse: 操作结果
    """
    if request.method == 'GET':
        # 获取请求参数
        product_id = request.GET.get('product_id')
        
        # 验证参数
        if not product_id:
            return APIResponse(code=1, msg='缺少商品ID')
        
        # 验证商品是否存在
        try:
            product = Product.objects.get(product_id=product_id, product_status=1)
        except Product.DoesNotExist:
            return APIResponse(code=1, msg='商品不存在')
        
        # 获取用户ID（从token中获取，如果没有token则为None）
        user_id = request.user.user_id if hasattr(request.user, 'user_id') else None
        
        # 如果有用户ID，记录浏览记录
        if user_id:
            # 检查是否已存在浏览记录，如果存在则更新时间
            record, created = Record.objects.get_or_create(
                user_id=user_id,
                product_id=product_id,
                defaults={'product_id': product_id}
            )
            
            if not created:
                # 更新创建时间为当前时间
                record.save()
            
            return APIResponse(code=0, msg='记录成功')
        
        # 如果没有用户ID，不记录但返回成功
        return APIResponse(code=0, msg='商品存在')


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def list_api(request):
    """
    获取用户浏览记录列表
    查询参数:
        page: 页码，默认1
        page_size: 每页数量，默认10
    Returns:
        APIResponse: 浏览记录列表和分页信息
    """
    if request.method == 'GET':
        # 获取用户ID
        user_id = request.user.user_id
        
        # 获取分页参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 查询浏览记录，按时间倒序
        records = Record.objects.filter(
            user_id=user_id
        ).order_by('-create_time')
        
        # 计算分页
        total = records.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_records = records[start:end]
        
        # 序列化
        serializer = RecordSerializer(page_records, many=True)
        
        # 返回结果
        return APIResponse(
            code=0,
            msg='查询成功',
            data={
                'list': serializer.data,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_page': (total + page_size - 1) // page_size
            }
        )


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def delete(request):
    """
    删除浏览记录
    请求体: {"record_id": 记录ID}
    Returns:
        APIResponse: 操作结果
    """
    if request.method == 'POST':
        # 获取用户ID
        user_id = request.user.user_id
        
        # 获取记录ID
        record_id = request.data.get('record_id')
        
        if not record_id:
            return APIResponse(code=1, msg='缺少记录ID')
        
        # 查找记录并删除
        try:
            record = Record.objects.get(record_id=record_id, user_id=user_id)
            record.delete()
            return APIResponse(code=0, msg='删除成功')
        except Record.DoesNotExist:
            return APIResponse(code=1, msg='记录不存在')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def deleteAll(request):
    """
    清空所有浏览记录
    Returns:
        APIResponse: 操作结果
    """
    if request.method == 'POST':
        # 获取用户ID
        user_id = request.user.user_id
        
        # 删除所有记录
        Record.objects.filter(user_id=user_id).delete()
        
        return APIResponse(code=0, msg='清空成功')