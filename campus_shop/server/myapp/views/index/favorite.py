"""
前台收藏视图模块
提供用户收藏商品的相关接口
"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import TokenAuthtication
from django.shortcuts import get_object_or_404

from myapp.handler import APIResponse
from myapp.models import Favorite, Product, UserInfo  # 添加UserInfo
from myapp.serializers import FavoriteSerializer


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def add(request):
    """
    添加收藏
    请求体: {"product_id": 商品ID}
    Returns:
        APIResponse: 操作结果
    """
    try:
        # 获取当前登录用户（使用TokenAuthtication方式）
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取商品ID
        product_id = request.data.get('product_id')
        
        if not product_id:
            return APIResponse(code=1, msg='缺少商品ID')
        
        # 验证商品是否存在且为在售状态
        try:
            product = Product.objects.get(product_id=product_id, product_status=1)
        except Product.DoesNotExist:
            return APIResponse(code=1, msg='商品不存在或不可收藏')
        
        # 检查是否已收藏
        if Favorite.objects.filter(user_id=user.user_id, product_id=product_id).exists():
            return APIResponse(code=1, msg='已收藏该商品')
        
        # 创建收藏
        favorite = Favorite.objects.create(
            user_id=user,
            product_id=product
        )
        
        serializer = FavoriteSerializer(favorite)
        return APIResponse(code=0, msg='收藏成功', data=serializer.data)
        
    except Exception as e:
        return APIResponse(code=1, msg='收藏失败', data=str(e))


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def remove(request):
    """
    取消收藏
    请求体: {"favorite_id": 收藏ID} 或 {"product_id": 商品ID}
    Returns:
        APIResponse: 操作结果
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取收藏ID或商品ID
        favorite_id = request.data.get('favorite_id')
        product_id = request.data.get('product_id')
        
        if not favorite_id and not product_id:
            return APIResponse(code=1, msg='缺少收藏ID或商品ID')
        
        # 根据收藏ID或商品ID删除
        if favorite_id:
            favorite = get_object_or_404(Favorite, favorite_id=favorite_id, user_id=user.user_id)
            favorite.delete()
        else:
            favorite = get_object_or_404(Favorite, user_id=user.user_id, product_id=product_id)
            favorite.delete()
        
        return APIResponse(code=0, msg='取消收藏成功')
        
    except Exception as e:
        return APIResponse(code=1, msg='取消收藏失败', data=str(e))


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def batchRemove(request):
    """
    批量取消收藏
    请求体: {"favorite_ids": [收藏ID1, 收藏ID2, ...]}
    Returns:
        APIResponse: 操作结果
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取收藏ID列表
        favorite_ids = request.data.get('favorite_ids', [])
        
        if not favorite_ids:
            return APIResponse(code=1, msg='缺少收藏ID列表')
        
        # 批量删除
        deleted_count, _ = Favorite.objects.filter(
            favorite_id__in=favorite_ids, 
            user_id=user.user_id
        ).delete()
        
        return APIResponse(code=0, msg=f'成功取消{deleted_count}个收藏')
        
    except Exception as e:
        return APIResponse(code=1, msg='批量取消失败', data=str(e))


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def list(request):
    """
    获取收藏列表
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取分页参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 查询收藏列表，按时间倒序
        favorites = Favorite.objects.filter(user_id=user.user_id).order_by('-create_time')
        
        # 计算分页
        total = favorites.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_favorites = favorites[start:end]
        
        # 序列化
        serializer = FavoriteSerializer(page_favorites, many=True)
        
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
        
    except Exception as e:
        return APIResponse(code=1, msg='查询失败', data=str(e))