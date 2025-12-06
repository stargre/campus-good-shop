"""
前台订单视图模块 - 校园二手交易平台
提供订单查询、创建、支付、确认收货、取消、评价等功能
以及商品预约相关功能
"""
import datetime
import random
import string

from rest_framework.decorators import api_view, authentication_classes, throttle_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.auth.throttling import MyRateThrottle
from myapp.handler import APIResponse
from myapp.models import UserOrder, Reserve, Product
from myapp.serializers import UserOrderSerializer, ReserveSerializer


@api_view(['GET'])
def list_api(request):
    """
    获取订单列表接口
    支持按用户ID和订单状态筛选
    Args:
        request: Django请求对象，GET参数包含userId和orderStatus
    Returns:
        APIResponse: 订单列表
    """
    if request.method == 'GET':
        userId = request.GET.get('userId', -1)
        orderStatus = request.GET.get('orderStatus', '')
        
        try:
            # 获取当前登录用户的订单
            orders = UserOrder.objects.filter(buyer_id=userId)
            
            # 如果指定了状态，进行筛选
            if orderStatus:
                orders = orders.filter(status=orderStatus)
                
            # 按创建时间倒序排列
            orders = orders.order_by('-create_time')
            
            serializer = UserOrderSerializer(orders, many=True)
            return APIResponse(code=0, msg='查询成功', data=serializer.data)
        except Exception as e:
            utils.log_error('订单列表查询失败', str(e))
            return APIResponse(code=1, msg='查询失败', data=str(e))


@api_view(['POST'])
@throttle_classes([MyRateThrottle])
@authentication_classes([TokenAuthentication])
def create(request):
    """
    创建订单接口
    Args:
        request: Django请求对象，包含product_id, buyer_id, seller_id, price等
    Returns:
        APIResponse: 创建结果
    """
    try:
        data = request.data.copy()
        
        # 验证必填参数
        if not data.get('product_id') or not data.get('buyer_id') or not data.get('seller_id'):
            return APIResponse(code=1, msg='参数不完整')
            
        # 检查商品是否存在且可购买
        product = Product.objects.get(pk=data['product_id'])
        if product.status != 1:  # 1表示在售
            return APIResponse(code=1, msg='商品已下架或不可购买')
            
        if product.seller_id == data['buyer_id']:
            return APIResponse(code=1, msg='不能购买自己发布的商品')
            
        # 生成订单号
        data['order_number'] = generate_order_number()
        data['create_time'] = datetime.datetime.now()
        data['status'] = 1  # 1表示待支付
        data['price'] = product.price  # 确保价格与商品一致
        
        # 创建订单
        serializer = UserOrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            # 更新商品状态为已预订
            product.status = 2  # 2表示已预订
            product.save()
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='创建失败', data=serializer.errors)
            
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        utils.log_error('创建订单失败', str(e))
        return APIResponse(code=1, msg='创建失败', data=str(e))

def generate_order_number():
    """
    生成唯一订单号
    """
    # 时间戳 + 随机字符串
    timestamp = str(utils.get_timestamp())
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return timestamp + random_str


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def cancel_order(request):
    """
    取消订单接口
    """
    try:
        order_id = request.GET.get('id', -1)
        order = UserOrder.objects.get(pk=order_id)
        
        # 只有待支付状态的订单可以取消
        if order.status != 1:
            return APIResponse(code=1, msg='该状态下订单不能取消')
            
        # 更新订单状态
        order.status = 5  # 5表示已取消
        order.save()
        
        # 恢复商品状态为在售
        product = Product.objects.get(pk=order.product_id)
        product.status = 1  # 1表示在售
        product.save()
        
        return APIResponse(code=0, msg='取消成功', data=UserOrderSerializer(order).data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        utils.log_error('取消订单失败', str(e))
        return APIResponse(code=1, msg='取消失败', data=str(e))

@api_view(['GET'])
def detail_api(request):
    """
    获取订单详情接口
    """
    try:
        order_id = request.GET.get('id', -1)
        order = UserOrder.objects.get(pk=order_id)
        
        serializer = UserOrderSerializer(order)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        utils.log_error('查询订单详情失败', str(e))
        return APIResponse(code=1, msg='查询失败', data=str(e))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def pay(request):
    """
    支付订单接口
    """
    try:
        order_id = request.POST.get('id', -1)
        order = UserOrder.objects.get(pk=order_id)
        
        # 只有待支付状态的订单可以支付
        if order.status != 1:
            return APIResponse(code=1, msg='订单状态不正确')
            
        # 模拟支付
        order.status = 2  # 2表示已支付
        order.pay_time = datetime.datetime.now()
        order.save()
        
        return APIResponse(code=0, msg='支付成功', data=UserOrderSerializer(order).data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        utils.log_error('支付订单失败', str(e))
        return APIResponse(code=1, msg='支付失败', data=str(e))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def confirm_receipt(request):
    """
    确认收货接口
    """
    try:
        order_id = request.POST.get('id', -1)
        order = UserOrder.objects.get(pk=order_id)
        
        # 只有已支付状态的订单可以确认收货
        if order.status != 2:
            return APIResponse(code=1, msg='订单状态不正确')
            
        order.status = 3  # 3表示已完成
        order.confirm_time = datetime.datetime.now()
        order.save()
        
        # 更新商品状态为已售出
        product = Product.objects.get(pk=order.product_id)
        product.status = 3  # 3表示已售出
        product.save()
        
        return APIResponse(code=0, msg='确认收货成功', data=UserOrderSerializer(order).data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        utils.log_error('确认收货失败', str(e))
        return APIResponse(code=1, msg='确认失败', data=str(e))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def evaluate(request):
    """
    评价订单接口
    """
    try:
        order_id = request.POST.get('id', -1)
        content = request.POST.get('content', '')
        rating = request.POST.get('rating', 5)
        
        order = UserOrder.objects.get(pk=order_id)
        
        # 只有已完成状态的订单可以评价
        if order.status != 3:
            return APIResponse(code=1, msg='订单状态不正确')
            
        # 只有买家可以评价
        if request.user.id != order.buyer_id:
            return APIResponse(code=1, msg='只有买家可以评价')
            
        order.evaluation_content = content
        order.evaluation_rating = rating
        order.evaluation_time = datetime.datetime.now()
        order.status = 4  # 4表示已评价
        order.save()
        
        return APIResponse(code=0, msg='评价成功', data=UserOrderSerializer(order).data)
        
    except UserOrder.DoesNotExist:
        return APIResponse(code=1, msg='订单不存在')
    except Exception as e:
        utils.log_error('评价订单失败', str(e))
        return APIResponse(code=1, msg='评价失败', data=str(e))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def reserve_create(request):
    """
    商品预约接口
    """
    try:
        data = request.data.copy()
        
        # 验证必填参数
        if not data.get('product_id') or not data.get('user_id'):
            return APIResponse(code=1, msg='参数不完整')
            
        # 检查商品是否存在且可预约
        product = Product.objects.get(pk=data['product_id'])
        if product.status != 1:  # 1表示在售
            return APIResponse(code=1, msg='商品已下架或不可预约')
            
        if product.seller_id == data['user_id']:
            return APIResponse(code=1, msg='不能预约自己发布的商品')
            
        # 检查是否已经预约
        existing_reserve = Reserve.objects.filter(product_id=data['product_id'], 
                                                 user_id=data['user_id'], 
                                                 status=1).first()  # 1表示有效预约
        if existing_reserve:
            return APIResponse(code=1, msg='您已经预约过该商品')
            
        # 创建预约
        data['create_time'] = datetime.datetime.now()
        data['status'] = 1  # 1表示有效预约
        
        serializer = ReserveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='预约成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='预约失败', data=serializer.errors)
            
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        utils.log_error('商品预约失败', str(e))
        return APIResponse(code=1, msg='预约失败', data=str(e))

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def reserve_list(request):
    """
    获取我的预约列表接口
    """
    try:
        user_id = request.GET.get('userId', -1)
        
        # 获取用户的所有预约
        reserves = Reserve.objects.filter(user_id=user_id).order_by('-create_time')
        
        serializer = ReserveSerializer(reserves, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
        
    except Exception as e:
        utils.log_error('查询预约列表失败', str(e))
        return APIResponse(code=1, msg='查询失败', data=str(e))

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def cancel_reserve(request):
    """
    取消预约接口
    """
    try:
        reserve_id = request.POST.get('id', -1)
        reserve = Reserve.objects.get(pk=reserve_id)
        
        # 只有有效预约可以取消
        if reserve.status != 1:
            return APIResponse(code=1, msg='预约状态不正确')
            
        reserve.status = 2  # 2表示已取消
        reserve.save()
        
        return APIResponse(code=0, msg='取消预约成功', data=ReserveSerializer(reserve).data)
        
    except Reserve.DoesNotExist:
        return APIResponse(code=1, msg='预约不存在')
    except Exception as e:
        utils.log_error('取消预约失败', str(e))
        return APIResponse(code=1, msg='取消失败', data=str(e))
