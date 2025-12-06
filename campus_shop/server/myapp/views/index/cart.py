"""
前台购物车视图模块
提供购物车相关接口
"""
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from myapp.auth.authentication import TokenAuthtication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from myapp.handler import APIResponse
from myapp.models import Cart, Product
from myapp.serializers import CartSerializer


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def list_api(request):
    """
    获取用户购物车列表
    Returns:
        APIResponse: 购物车列表
    """
    if request.method == 'GET':
        # 获取用户ID
        user_id = request.user.user_id
        
        # 查询购物车
        carts = Cart.objects.filter(user_id=user_id).order_by('-add_time')
        
        # 序列化
        serializer = CartSerializer(carts, many=True)
        
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def add(request):
    """
    添加商品到购物车
    请求体: {"product_id": 商品ID}
    Returns:
        APIResponse: 操作结果
    """
    if request.method == 'POST':
        # 获取用户ID
        user_id = request.user.user_id
        
        # 获取商品ID
        product_id = request.data.get('product_id')
        
        if not product_id:
            return APIResponse(code=1, msg='缺少商品ID')
        
        # 验证商品是否存在
        try:
            product = Product.objects.get(product_id=product_id, product_status=1)
        except Product.DoesNotExist:
            return APIResponse(code=1, msg='商品不存在')
        
        # 检查是否已在购物车中
        existing_cart = Cart.objects.filter(user_id=user_id, product_id=product_id).first()
        if existing_cart:
            return APIResponse(code=0, msg='已在购物车中')
        
        # 添加到购物车
        cart = Cart(user_id=user_id, product_id=product_id)
        cart.save()
        
        return APIResponse(code=0, msg='添加成功')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def delete(request):
    """
    从购物车移除商品
    请求体: {"cart_id": 购物车ID}
    Returns:
        APIResponse: 操作结果
    """
    if request.method == 'POST':
        # 获取用户ID
        user_id = request.user.user_id
        
        # 获取购物车ID
        cart_id = request.data.get('cart_id')
        
        if not cart_id:
            return APIResponse(code=1, msg='缺少购物车ID')
        
        # 查找并删除
        try:
            cart = Cart.objects.get(cart_id=cart_id, user_id=user_id)
            cart.delete()
            return APIResponse(code=0, msg='删除成功')
        except Cart.DoesNotExist:
            return APIResponse(code=1, msg='购物车商品不存在')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
@permission_classes([IsAuthenticated])
def deleteAll(request):
    """
    清空购物车
    Returns:
        APIResponse: 操作结果
    """
    if request.method == 'POST':
        # 获取用户ID
        user_id = request.user.user_id
        
        # 清空购物车
        Cart.objects.filter(user_id=user_id).delete()
        
        return APIResponse(code=0, msg='清空成功')