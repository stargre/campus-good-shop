"""
前台购物车视图模块 - 修复版
提供购物车相关接口
"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Cart, Product, UserInfo
from myapp.serializers import CartSerializer


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def list_api(request):
    """
    获取用户购物车列表 - 修复版
    """
    try:
        # 获取当前登录用户（使用你的认证方式）
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 查询购物车
        carts = Cart.objects.filter(user_id=user.user_id).order_by('-add_time')
        
        # 序列化
        serializer = CartSerializer(carts, many=True)
        
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Exception as e:
        print(f"购物车列表错误: {str(e)}")
        return APIResponse(code=1, msg='查询失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def add(request):
    """
    添加商品到购物车 - 修复版
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取商品ID
        product_id = request.data.get('product_id')
        if not product_id:
            return APIResponse(code=1, msg='缺少商品ID')
        
        # 验证商品是否存在且可购买（状态1=审核通过）
        try:
            product = Product.objects.get(product_id=product_id, product_status=1)
        except Product.DoesNotExist:
            return APIResponse(code=1, msg='商品不存在或不可购买')
        
        # 检查是否已在购物车中
        if Cart.objects.filter(user_id=user.user_id, product_id=product_id).exists():
            return APIResponse(code=0, msg='已在购物车中')
        
        # 添加到购物车
        cart = Cart.objects.create(
            user_id=user,
            product_id=product
        )
        
        return APIResponse(code=0, msg='添加成功')
    except Exception as e:
        print(f"添加购物车错误: {str(e)}")
        return APIResponse(code=1, msg='添加失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def delete(request):
    """
    从购物车移除商品 - 修复版
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取购物车ID
        cart_id = request.data.get('cart_id')
        if not cart_id:
            return APIResponse(code=1, msg='缺少购物车ID')
        
        # 查找并删除
        try:
            cart = Cart.objects.get(cart_id=cart_id, user_id=user.user_id)
            cart.delete()
            return APIResponse(code=0, msg='删除成功')
        except Cart.DoesNotExist:
            return APIResponse(code=1, msg='购物车商品不存在')
    except Exception as e:
        print(f"删除购物车错误: {str(e)}")
        return APIResponse(code=1, msg='删除失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def deleteAll(request):
    """
    清空购物车 - 修复版
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 清空购物车
        Cart.objects.filter(user_id=user.user_id).delete()
        
        return APIResponse(code=0, msg='清空成功')
    except Exception as e:
        print(f"清空购物车错误: {str(e)}")
        return APIResponse(code=1, msg='清空失败')