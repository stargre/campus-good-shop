"""后台评论管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Comment, UserInfo
from myapp.serializers import CommentSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """评论列表接口"""
    try:
        # 获取查询参数
        keyword = request.GET.get('keyword', '')
        seller_id = request.GET.get('seller_id', '')
        buyer_id = request.GET.get('buyer_id', '')
        comment_status = request.GET.get('comment_status', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 基础查询集
        comments = Comment.objects.all()
        
        # 关键词搜索（评论内容、买家/卖家名称）
        if keyword:
            comments = comments.filter(
                Q(comment_content__contains=keyword) |
                Q(user_id__user_name__contains=keyword) |
                Q(seller_id__user_name__contains=keyword)
            )
        
        # 卖家筛选
        if seller_id:
            comments = comments.filter(seller_id=seller_id)
        
        # 买家筛选
        if buyer_id:
            comments = comments.filter(user_id=buyer_id)
        
        # 评论状态筛选
        if comment_status:
            comments = comments.filter(comment_status=int(comment_status))
        
        # 时间范围筛选
        if start_date:
            comments = comments.filter(create_time__gte=start_date)
        if end_date:
            comments = comments.filter(create_time__lte=end_date)
        
        # 总数
        total = comments.count()
        
        # 分页（按评论时间倒序）
        start = (page - 1) * page_size
        end = start + page_size
        comments = comments.order_by('-create_time')[start:end]
        
        # 序列化
        serializer = CommentSerializer(comments, many=True)
        
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """新增评论接口"""
    try:
        # 获取评论数据（支持按订单或商品进行评论）
        order_id = request.data.get('order_id')
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        seller_id = request.data.get('seller_id')
        comment_content = request.data.get('comment_content', '')
        rating = int(request.data.get('rating', 10))
        comment_status = int(request.data.get('comment_status', 0))

        if not user_id:
            return APIResponse(code=1, msg='缺少用户ID')

        # 尝试从订单或商品推导卖家ID
        from myapp.models import UserOrder, Product
        if not seller_id:
            if order_id:
                try:
                    order = UserOrder.objects.get(order_id=order_id)
                    seller_id = order.seller_id.user_id
                except UserOrder.DoesNotExist:
                    return APIResponse(code=1, msg='订单不存在')
            elif product_id:
                try:
                    product = Product.objects.get(product_id=product_id)
                    seller_id = product.user_id.user_id
                except Product.DoesNotExist:
                    return APIResponse(code=1, msg='商品不存在')
            else:
                return APIResponse(code=1, msg='缺少订单ID或商品ID')

        # 构建评论数据
        comment_data = {
            'order_id': order_id,
            'product_id': product_id,
            'user_id': user_id,
            'seller_id': seller_id,
            'comment_content': comment_content,
            'rating': rating,
            'comment_status': comment_status,
        }

        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='评论创建成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
            
    except Exception as e:
        return APIResponse(code=1, msg=f'创建评论失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新评论状态（审核评论）"""
    try:
        comment_id = request.data.get('comment_id')
        comment_status = request.data.get('comment_status')
        
        if not comment_id:
            return APIResponse(code=1, msg='评论ID不能为空')
        
        comment = Comment.objects.get(comment_id=comment_id)
        
        # 更新评论状态
        if comment_status is not None:
            comment.comment_status = int(comment_status)
            comment.save()
        
        serializer = CommentSerializer(comment)
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
        
    except Comment.DoesNotExist:
        return APIResponse(code=1, msg='评论不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'更新失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除评论接口"""
    try:
        ids_param = request.GET.get('ids') or request.data.get('ids')
        if ids_param:
            ids = [s.strip() for s in str(ids_param).split(',') if s.strip()]
            deleted = 0
            for sid in ids:
                try:
                    cid = int(sid)
                    comment = Comment.objects.get(comment_id=cid)
                    comment.delete()
                    deleted += 1
                except (ValueError, Comment.DoesNotExist):
                    continue
            if deleted == 0:
                return APIResponse(code=1, msg='评论不存在')
            return APIResponse(code=0, msg='删除成功')

        comment_id = request.data.get('comment_id') or request.GET.get('comment_id')
        if not comment_id:
            return APIResponse(code=1, msg='评论ID不能为空')
        comment = Comment.objects.get(comment_id=int(comment_id))
        comment.delete()
        return APIResponse(code=0, msg='删除成功')
        
    except Comment.DoesNotExist:
        return APIResponse(code=1, msg='评论不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')
