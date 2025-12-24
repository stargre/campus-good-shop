"""
前台评论视图模块
提供商品评论的查询、创建、点赞等接口
"""
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from datetime import datetime

from myapp.auth.authentication import TokenAuthtication
from myapp.auth.throttling import MyRateThrottle
from myapp.handler import APIResponse
from myapp.models import Comment, UserInfo, Product
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import CommentSerializer


def get_current_user(request):
    """获取当前登录用户（TokenAuthtication方式）"""
    token = request.META.get("HTTP_TOKEN", "")
    users = UserInfo.objects.filter(token=token)
    if len(users) == 0:
        return None
    return users[0]


@api_view(['GET'])
def list_api(request):
    """
    获取评论列表接口
    支持按商品ID查询，支持按时间或点赞数排序
    Args:
        request: Django请求对象，GET参数包含productId（商品ID）和order（排序方式）
    Returns:
        APIResponse: 评论列表
    """
    if request.method == 'GET':
        productId = request.GET.get("productId", None)
        order = request.GET.get("order", 'recent')

        if productId:
            if order == 'recent':
                orderBy = '-create_time'
            else:
                orderBy = '-rating'

            comments = Comment.objects.select_related("product_id").filter(product_id=productId).order_by(orderBy)
            serializer = CommentSerializer(comments, many=True)
            return APIResponse(code=0, msg='查询成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='productId不能为空')


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def list_my_comment(request):
    """
    获取用户自己的评论列表接口
    Args:
        request: Django请求对象，GET参数包含order（排序方式）
    Returns:
        APIResponse: 用户评论列表
    """
    if request.method == 'GET':
        user = get_current_user(request)
        if not user:
            return APIResponse(code=1, msg='用户未登录')
            
        order = request.GET.get("order", 'recent')

        if order == 'recent':
            orderBy = '-create_time'
        else:
            orderBy = '-rating'

        comments = Comment.objects.select_related("product_id").filter(user_id=user.user_id).order_by(orderBy)
        serializer = CommentSerializer(comments, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):
    """
    创建商品评论接口
    请求体: {"content": "评论内容", "product": "商品ID"}
    Returns:
        APIResponse: 操作结果
    """
    try:
        user = get_current_user(request)
        if not user:
            return APIResponse(code=1, msg='用户未登录')
        
        # 获取评论数据（兼容字段名 product / product_id）
        # 兼容JSON与表单提交
        content = (request.data.get('content') or request.POST.get('content') or '').strip()
        product_field = (
            request.data.get('product') or request.data.get('product_id') or
            request.POST.get('product') or request.POST.get('product_id')
        )
        if not content or not product_field:
            return APIResponse(code=1, msg='评论内容和商品ID不能为空')
        
        # 验证商品是否存在（兼容字符串ID）
        try:
            pid = int(product_field)
            product = Product.objects.get(pk=pid)
        except (ValueError, TypeError):
            return APIResponse(code=1, msg='商品ID格式不正确')
        except Product.DoesNotExist:
            return APIResponse(code=1, msg='商品不存在')
        
        # 使用序列化器创建，传递外键ID
        from django.utils import timezone
        comment = Comment.objects.create(
            product_id=product,
            user_id=user,
            seller_id=product.user_id,
            comment_content=content,
            rating=10,
            comment_status=0,
            create_time=timezone.now(),
        )
        serializer = CommentSerializer(comment)
        return APIResponse(code=0, msg='评论成功', data=serializer.data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"创建评论失败: {e}")
        return APIResponse(code=1, msg='评论失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def delete(request):
    """
    删除评论接口
    请求体: {"ids": "评论ID"} 或 GET参数: {"ids": "评论ID"}
    Returns:
        APIResponse: 操作结果
    """
    try:
        # 支持从GET参数或POST body获取ids
        ids = request.GET.get('ids') or request.data.get('ids')
        if not ids:
            return APIResponse(code=1, msg='ids不能为空')
            
        ids_arr = ids.split(',')
        Comment.objects.filter(comment_id__in=ids_arr).delete()
    except Comment.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')

    return APIResponse(code=0, msg='删除成功')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def like(request):
    """
    评论点赞接口
    请求体或GET参数: {"commentId": "评论ID"}
    Returns:
        APIResponse: 操作结果
    """
    try:
        user = get_current_user(request)
        if not user:
            return APIResponse(code=1, msg='用户未登录')
            
        # 支持从GET参数或POST body获取commentId
        commentId = request.data.get('commentId') or request.GET.get('commentId')
        if not commentId:
            return APIResponse(code=1, msg='commentId不能为空')
            
        comment = Comment.objects.get(pk=commentId)
        comment.save()
    except Comment.DoesNotExist:
        return APIResponse(code=1, msg='评论不存在')
    except Exception as e:
        print(f"点赞失败: {e}")
        return APIResponse(code=1, msg='点赞失败')

    return APIResponse(code=0, msg='点赞成功')
