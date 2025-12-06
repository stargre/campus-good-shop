"""
前台地址视图模块
提供用户收货地址的查询、创建、更新、删除接口
"""
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Address
from myapp.serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def list_api(request):
    """
    获取用户地址列表
    Returns:
        APIResponse: 地址列表
    """
    if request.method == 'GET':
        # 获取用户ID
        user_id = request.user.user_id if hasattr(request.user, 'user_id') else None
        
        if user_id:
            addresses = Address.objects.filter(user_id=user_id).order_by('-address_id')
            serializer = AddressSerializer(addresses, many=True)
            return APIResponse(code=0, msg='查询成功', data=serializer.data)
        else:
            # 从查询参数获取用户ID（兼容前端）
            user_id = request.GET.get('user_id')
            if user_id:
                addresses = Address.objects.filter(user_id=user_id).order_by('-address_id')
                serializer = AddressSerializer(addresses, many=True)
                return APIResponse(code=0, msg='查询成功', data=serializer.data)
            return APIResponse(code=1, msg='缺少用户ID')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):
    """
    创建新地址
    请求体: {"receiver_name": "收货人姓名", "receiver_phone": "电话号码", "receiver_address": "详细地址", "is_default": 0}
    Returns:
        APIResponse: 操作结果
    """
    # 获取用户ID
    user_id = request.user.user_id
    
    # 从请求体获取数据
    data = request.data.copy()
    data['user_id'] = user_id
    
    # 检查是否设为默认地址
    if data.get('is_default') == 1:
        # 将用户其他地址设为非默认
        Address.objects.filter(user_id=user_id).update(is_default=0)
    
    # 验证并保存
    serializer = AddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    return APIResponse(code=1, msg='参数错误', data=serializer.errors)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def update(request):
    """
    更新地址
    请求体: {"address_id": "地址ID", "receiver_name": "收货人姓名", "receiver_phone": "电话号码", "receiver_address": "详细地址", "is_default": 0}
    Returns:
        APIResponse: 操作结果
    """
    # 获取用户ID
    user_id = request.user.user_id
    
    # 获取地址ID
    address_id = request.data.get('address_id')
    
    if not address_id:
        return APIResponse(code=1, msg='缺少地址ID')
    
    # 查找地址
    try:
        address = Address.objects.get(address_id=address_id, user_id=user_id)
    except Address.DoesNotExist:
        return APIResponse(code=1, msg='地址不存在')
    
    # 从请求体获取数据
    data = request.data.copy()
    data['user_id'] = user_id
    
    # 检查是否设为默认地址
    if data.get('is_default') == 1:
        # 将用户其他地址设为非默认
        Address.objects.filter(user_id=user_id).update(is_default=0)
    
    # 验证并保存
    serializer = AddressSerializer(address, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    return APIResponse(code=1, msg='参数错误', data=serializer.errors)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def delete(request):
    """
    删除地址
    请求体: {"address_id": "地址ID"}
    Returns:
        APIResponse: 操作结果
    """
    # 获取用户ID
    user_id = request.user.user_id
    
    # 获取地址ID
    address_id = request.data.get('address_id')
    
    if not address_id:
        return APIResponse(code=1, msg='缺少地址ID')
    
    # 删除地址
    try:
        address = Address.objects.get(address_id=address_id, user_id=user_id)
        address.delete()
        return APIResponse(code=0, msg='删除成功')
    except Address.DoesNotExist:
        return APIResponse(code=1, msg='地址不存在')
