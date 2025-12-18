"""
前台订单视图模块 - 校园二手交易平台（修复版）
提供订单查询、创建、支付、确认收货、取消、评价等功能
"""
import datetime
import random
import string

from rest_framework.decorators import api_view, authentication_classes
from django.db.models import Q
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import UserOrder, Product, UserInfo, Comment
from myapp.serializers import UserOrderSerializer, CommentSerializer


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def list_api(request):
    """
    获取订单列表接口（修复版）
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取查询参数
        order_status = request.GET.get('orderStatus', '')
        
        # 构建查询条件：用户是买家或卖家
        orders = UserOrder.objects.filter(
            Q(user_id=user.user_id) | Q(seller_id=user.user_id)
        )
        
        # 状态筛选
        if order_status:
            orders = orders.filter(order_status=int(order_status))
        
        # 按创建时间倒序排列
        orders = orders.order_by('-create_time')
        
        serializer = UserOrderSerializer(orders, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Exception as e:
        print(f"订单列表查询失败: {str(e)}")
        return APIResponse(code=1, msg='查询失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):
    """
    创建订单接口（修复版）
    """
    try:
        # 获取当前登录用户（买家）
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        buyer = users[0]
        
        data = request.data.copy()
        
        # 验证必填参数
        product_id = data.get('product_id')
        if not product_id:
            return APIResponse(code=1, msg='商品ID不能为空')
        
        # 获取商品
        product = Product.objects.get(product_id=product_id)
        
        # 检查商品状态（1=审核通过）
        if product.product_status != 1:
            return APIResponse(code=1, msg='商品不可购买')
        
        # 检查是否购买自己的商品
        if product.user_id.user_id == buyer.user_id:
            return APIResponse(code=1, msg='不能购买自己发布的商品')
        
        # 构建订单数据
        order_data = {
            'user_id': buyer.user_id,  # 买家
            'seller_id': product.user_id.user_id,  # 卖家
            'product_id': product_id,
            'product_title': product.product_title,
            'product_image': '',  # 需要从商品图片获取第一张
            'price': product.product_price,  # 与数据库与前端保持一致（单位：元，整数）
            'order_status': 0,  # 0=待支付
        }
        
        # 获取商品第一张图片
        from myapp.models import ProductImage
        images = ProductImage.objects.filter(product_id=product_id).order_by('sort_order')
        if images.exists():
            order_data['product_image'] = images.first().image_url
        else:
            order_data['product_image'] = ''
        
        # 创建订单
        serializer = UserOrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            
            # 更新商品状态为已售出（或者保留原状态，等支付完成再改）
            # product.product_status = 3  # 3=已售出
            # product.save()
            
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        else:
            print("订单序列化错误:", serializer.errors)
            return APIResponse(code=1, msg='创建失败', data=serializer.errors)
            
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        print(f"创建订单失败: {str(e)}")
        return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def cancel_order(request):
    """
    取消订单接口（修复版）
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        order_id = request.data.get('order_id')
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')
        
        order = UserOrder.objects.get(order_id=order_id)
        
        # 检查权限：只有买家可以取消订单
        if order.user_id.user_id != user.user_id:
            return APIResponse(code=1, msg='无权取消此订单')
        
        # 只有待支付状态的订单可以取消
        if order.order_status != 0:
            return APIResponse(code=1, msg='该状态下订单不能取消')
        
        # 更新订单状态为已取消
        order.order_status = 4  # 4=已取消
        order.cancel_time = datetime.datetime.now()
        order.save()
        
        # 恢复商品状态为审核通过
        product = order.product_id
        product.product_status = 1  # 1=审核通过
        product.save()
        
        return APIResponse(code=0, msg='取消成功', data=UserOrderSerializer(order).data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        print(f"取消订单失败: {str(e)}")
        return APIResponse(code=1, msg='取消失败')


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def detail_api(request):
    """
    获取订单详情接口（修复版）
    """
    try:
        order_id = request.GET.get('id')
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')
        
        order = UserOrder.objects.get(order_id=order_id)
        serializer = UserOrderSerializer(order)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        print(f"查询订单详情失败: {str(e)}")
        return APIResponse(code=1, msg='查询失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def pay(request):
    """
    支付订单接口（修复版）
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        order_id = request.data.get('order_id')
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')
        
        order = UserOrder.objects.get(order_id=order_id)
        
        # 检查权限：只有买家可以支付
        if order.user_id.user_id != user.user_id:
            return APIResponse(code=1, msg='无权支付此订单')
        
        # 只有待支付状态的订单可以支付
        if order.order_status != 0:
            return APIResponse(code=1, msg='订单状态不正确')
        
        # 检查商品是否已被售出（被其他订单支付）
        product = order.product_id
        if product.product_status == 3:
            return APIResponse(code=1, msg='商品已售出，无法支付')

        # 模拟支付：更新状态为已支付
        order.order_status = 1  # 1=已支付
        order.pay_time = datetime.datetime.now()
        order.save()
        
        # 更新商品状态为已售出
        product.product_status = 3  # 3=已售出
        product.save()
        
        return APIResponse(code=0, msg='支付成功', data=UserOrderSerializer(order).data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        print(f"支付订单失败: {str(e)}")
        return APIResponse(code=1, msg='支付失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def confirm_receipt(request):
    """
    确认收货接口（修复版）
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        order_id = request.data.get('order_id')
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')
        
        order = UserOrder.objects.get(order_id=order_id)
        
        # 检查权限：只有买家可以确认收货
        if order.user_id.user_id != user.user_id:
            return APIResponse(code=1, msg='无权确认此订单')
        
        # 只有已支付状态的订单可以确认收货
        if order.order_status != 1:
            return APIResponse(code=1, msg='订单状态不正确')
        
        # 更新状态为已完成
        order.order_status = 3  # 3=已完成
        order.receive_time = datetime.datetime.now()  # 修复字段名
        order.save()
        
        return APIResponse(code=0, msg='确认收货成功', data=UserOrderSerializer(order).data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        print(f"确认收货失败: {str(e)}")
        return APIResponse(code=1, msg='确认失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def evaluate(request):
    """
    评价订单接口（修复版）- 使用独立的Comment模型
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        order_id = request.data.get('order_id')
        comment_content = request.data.get('content', '')
        rating = request.data.get('rating', 10)  # 默认10分
        
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')
        
        order = UserOrder.objects.get(order_id=order_id)
        
        # 检查权限：只有买家可以评价
        if order.user_id.user_id != user.user_id:
            return APIResponse(code=1, msg='只有买家可以评价')
        
        # 只有已完成状态的订单可以评价
        if order.order_status != 3:
            return APIResponse(code=1, msg='订单状态不正确')
        
        # 检查是否已评价过
        if Comment.objects.filter(order_id=order_id).exists():
            return APIResponse(code=1, msg='该订单已评价过')
        
        # 创建评价
        comment_data = {
            'order_id': order.order_id,
            'user_id': user.user_id,  # 买家
            'seller_id': order.seller_id.user_id,  # 卖家
            'comment_content': comment_content,
            'rating': rating,
            'comment_status': 0  # 0=正常
        }
        
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='评价成功', data=serializer.data)
        else:
            print("评价序列化错误:", serializer.errors)
            return APIResponse(code=1, msg='评价失败', data=serializer.errors)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        print(f"评价订单失败: {str(e)}")
        return APIResponse(code=1, msg='评价失败')
from django.utils import timezone
from myapp.models import UserOrder
from myapp.handler import APIResponse
from myapp.auth.authentication import TokenAuthtication
from rest_framework.decorators import api_view, authentication_classes

@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def deliver(request):
    """卖家发货：将已支付(1)的订单更新为已发货(2)"""
    try:
        order_id = request.data.get('order_id')
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')
        try:
            order = UserOrder.objects.get(order_id=order_id)
        except UserOrder.DoesNotExist:
            return APIResponse(code=1, msg='订单不存在')

        if int(order.order_status) != 1:
            return APIResponse(code=1, msg='仅已支付订单可发货')

        order.order_status = 2
        if hasattr(order, 'deliver_time'):
            order.deliver_time = timezone.now()
        order.update_time = timezone.now()
        order.save()
        return APIResponse(code=0, msg='发货成功', data={
            'order_id': order.order_id,
            'order_status': order.order_status
        })
    except Exception as e:
        return APIResponse(code=1, msg=f'发货失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def refund(request):
    """商家退款接口（仅限卖家在发货前退款）"""
    try:
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]

        order_id = request.data.get('order_id')
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')

        try:
            order = UserOrder.objects.get(order_id=order_id)
        except UserOrder.DoesNotExist:
            return APIResponse(code=1, msg='订单不存在')

        # 只有已支付状态的订单可以退款，并且必须由卖家发起
        if order.order_status != 1:
            return APIResponse(code=1, msg='该订单不是可退款状态')
        if order.seller_id.user_id != user.user_id:
            return APIResponse(code=1, msg='无权退款')

        # 执行退款：更新订单状态为已退款，并恢复商品状态
        order.order_status = 5  # 5=已退款
        order.update_time = timezone.now()
        order.save()

        product = order.product_id
        product.product_status = 1  # 恢复为审核通过
        product.save()

        return APIResponse(code=0, msg='退款成功', data=UserOrderSerializer(order).data)
    except Exception as e:
        return APIResponse(code=1, msg=f'退款失败: {str(e)}')
