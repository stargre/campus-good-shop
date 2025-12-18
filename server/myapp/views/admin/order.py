"""
后台订单管理视图模块
"""
from rest_framework.decorators import api_view, authentication_classes
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import UserOrder, UserInfo, Product
from myapp.serializers import UserOrderSerializer, ListUserOrderSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """订单列表接口"""
    try:
        # 获取查询参数
        order_status = request.GET.get('order_status') or request.GET.get('status', None)
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size') or request.GET.get('pageSize', 10))
        
        # 基础查询集
        orders = UserOrder.objects.all()
        
        # 状态筛选
        if order_status is not None:
            orders = orders.filter(order_status=int(order_status))
        
        # 关键词搜索（买家、卖家、商品标题）
        if keyword:
            orders = orders.filter(
                Q(product_title__contains=keyword) |
                Q(user_id__user_name__contains=keyword) |
                Q(seller_id__user_name__contains=keyword)
            )
        
        # 总数
        total = orders.count()
        
        # 分页（按创建时间倒序）
        start = (page - 1) * page_size
        end = start + page_size
        orders = orders.order_by('-create_time')[start:end]
        
        # 序列化（使用简化的列表序列化器）
        serializer = ListUserOrderSerializer(orders, many=True)
        
        return APIResponse(code=0, msg='查询成功', data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def detail(request):
    """订单详情接口"""
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
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新订单状态接口"""
    try:
        order_id = request.data.get('order_id') or request.GET.get('order_id')
        new_status = request.data.get('order_status') or request.GET.get('order_status')
        
        if not order_id or new_status is None:
            return APIResponse(code=1, msg='订单ID和状态不能为空')
        
        order = UserOrder.objects.get(order_id=order_id)
        
        # 管理后台允许直接设置任意状态
        old_status = order.order_status
        new_status = int(new_status)
        
        # 更新状态
        order.order_status = new_status
        
        # 根据状态设置相关时间
        from django.utils import timezone
        if new_status == 1:  # 已支付
            order.pay_time = timezone.now()
        elif new_status == 3:  # 已完成
            order.receive_time = timezone.now()
        elif new_status == 4:  # 已取消
            order.cancel_time = timezone.now()
        
        order.save()
        
        # 如果订单完成，更新商品状态为已售出
        if new_status == 3:  # 已完成
            product = order.product_id
            product.product_status = 3  # 已售出
            product.save()
        
        serializer = UserOrderSerializer(order)
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'更新失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """
    创建订单接口（后台管理专用）
    """
    try:
        data = request.data.copy()
        
        # 必填字段验证
        required_fields = ['user_id', 'seller_id', 'product_id', 'price']
        for field in required_fields:
            if not data.get(field):
                return APIResponse(code=1, msg=f'{field}不能为空')
        
        # 检查用户是否存在
        try:
            buyer = UserInfo.objects.get(user_id=data['user_id'])
            seller = UserInfo.objects.get(user_id=data['seller_id'])
        except UserInfo.DoesNotExist:
            return APIResponse(code=1, msg='用户不存在')
        
        # 检查商品是否存在
        try:
            product = Product.objects.get(product_id=data['product_id'])
        except Product.DoesNotExist:
            return APIResponse(code=1, msg='商品不存在')
        
        # 构建订单数据
        order_data = {
            'user_id': buyer,
            'seller_id': seller,
            'product_id': product,
            'product_title': product.product_title,
            'product_image': '',  # 获取商品第一张图片
            'price': data['price'],
            'order_status': data.get('order_status', 0)  # 默认待支付
        }
        
        # 获取商品第一张图片
        from myapp.models import ProductImage
        images = ProductImage.objects.filter(product_id=product.product_id).order_by('sort_order')
        if images.exists():
            order_data['product_image'] = images.first().image_url
        
        # 创建订单
        order = UserOrder.objects.create(**order_data)
        
        # 序列化返回
        serializer = UserOrderSerializer(order)
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
        
    except Exception as e:
        return APIResponse(code=1, msg=f'创建失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """
    删除订单接口（谨慎使用）
    """
    try:
        order_id = request.data.get('order_id') or request.GET.get('order_id')
        if not order_id:
            return APIResponse(code=1, msg='订单ID不能为空')
        
        order = UserOrder.objects.get(order_id=order_id)
        
        # 检查订单状态，某些状态下不能删除
        if order.order_status not in [4, 5]:  # 只允许删除已取消或已退款的订单
            return APIResponse(code=1, msg='只有已取消或已退款的订单可以删除')
        
        order.delete()
        
        return APIResponse(code=0, msg='删除成功')
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')


# 注意：根据业务需求，以下接口可能不需要或不适合在后台实现
# 取消订单（应该由用户操作）
# 延期订单（根据具体业务需求）
