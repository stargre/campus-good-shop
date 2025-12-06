"""
前台商品视图模块
实现二手商品的发布、查询、更新、删除等功能
"""
import json
from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from django.db.models import Q, F
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Product, ProductImage, UserInfo, Reserve, Record
from myapp.serializers import ProductSerializer, ProductDetailSerializer


@api_view(['GET'])
def list(request):
    """
    获取商品列表接口
    Args:
        request: Django请求对象，支持分类过滤、搜索、分页等参数
    Returns:
        APIResponse: 商品列表数据
    """
    try:
        # 基本查询参数
        category_id = request.GET.get('category_id', None)
        keyword = request.GET.get('keyword', None)
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        
        # 高级筛选参数
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)
        quality = request.GET.get('quality', None)
        status = request.GET.get('status', None)
        
        # 排序参数
        sort = request.GET.get('sort', 'create_time')  # 默认按创建时间排序
        order = request.GET.get('order', 'desc')  # 默认降序
        
        # 构建查询条件
        query = Q()
        if category_id:
            query &= Q(category_id=category_id)
        if keyword:
            query &= (Q(product_title__contains=keyword) | Q(product_desc__contains=keyword))
        if min_price:
            query &= Q(product_price__gte=int(min_price))
        if max_price:
            query &= Q(product_price__lte=int(max_price))
        if quality:
            query &= Q(product_quality=quality)
        if status:
            query &= Q(product_status=status)
        
        # 应用查询条件
        products = Product.objects.filter(query)
        
        # 应用排序
        order_by = sort
        if order == 'desc':
            order_by = f'-{sort}'
        products = products.order_by(order_by)
        
        # 计算总数
        total = products.count()
        
        # 分页
        products = products[(page - 1) * size: page * size]
        
        # 序列化
        serializer = ProductSerializer(products, many=True)
        
        # 构建返回数据
        data = {
            'list': serializer.data,
            'pagination': {
                'page': page,
                'size': size,
                'total': total,
                'total_page': (total + size - 1) // size
            }
        }
        
        return APIResponse(code=0, msg='查询成功', data=data)
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='查询失败')


@api_view(['GET'])
def detail(request):
    """
    获取商品详情接口
    Args:
        request: Django请求对象，包含商品ID参数
    Returns:
        APIResponse: 商品详情数据
    """
    try:
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
        
        # 记录浏览历史
        try:
            # 如果用户已登录，记录用户浏览记录
            token = request.META.get("HTTP_TOKEN", "")
            if token:
                users = UserInfo.objects.filter(token=token)
                if len(users) > 0:
                    user = users[0]
                    # 检查是否已存在该用户对该商品的浏览记录
                    record_exists = Record.objects.filter(user_id=user, product_id=product).exists()
                    if not record_exists:
                        Record.objects.create(
                            user_id=user,
                            product_id=product,
                            record_time=datetime.now()
                        )
            
            # 增加浏览量
            Product.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
        except Exception as e:
            print(f"记录浏览历史失败: {e}")
        
        # 序列化，使用包含完整信息的序列化器
        serializer = ProductDetailSerializer(product)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='查询失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):
    """
    创建商品接口
    Args:
        request: Django请求对象，包含商品信息
    Returns:
        APIResponse: 创建结果
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 添加用户ID到请求数据
        data = request.data.copy()
        data['user_id'] = user.user_id
        
        # 将价格从元转换为分（整数存储）
        if 'product_price' in data and data['product_price']:
            try:
                data['product_price'] = int(float(data['product_price']) * 100)
            except (ValueError, TypeError):
                return APIResponse(code=1, msg='价格格式不正确')
        
        # 创建商品
        serializer = ProductDetailSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            
            # 处理商品图片
            if 'images' in data:
                images = json.loads(data['images'])
                for img_url in images:
                    ProductImage.objects.create(
                        product_id=product,
                        img_url=img_url
                    )
            
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        else:
            print(serializer.errors)
            return APIResponse(code=1, msg='创建失败', data=serializer.errors)
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def update(request):
    """
    更新商品接口
    Args:
        request: Django请求对象，包含商品ID和要更新的信息
    Returns:
        APIResponse: 更新结果
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取商品ID
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
        
        # 检查是否是商品发布者
        if product.user_id.user_id != user.user_id:
            return APIResponse(code=1, msg='无权操作此商品')
        
        # 处理价格转换
        data = request.data.copy()
        if 'product_price' in data and data['product_price']:
            try:
                data['product_price'] = int(float(data['product_price']) * 100)
            except (ValueError, TypeError):
                return APIResponse(code=1, msg='价格格式不正确')
        
        # 更新商品信息
        serializer = ProductDetailSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # 更新商品图片
            if 'images' in data:
                # 删除原有的图片
                ProductImage.objects.filter(product_id=product).delete()
                # 添加新的图片
                images = json.loads(data['images'])
                for img_url in images:
                    ProductImage.objects.create(
                        product_id=product,
                        img_url=img_url
                    )
            
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            print(serializer.errors)
            return APIResponse(code=1, msg='更新失败', data=serializer.errors)
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def delete(request):
    """
    删除商品接口
    Args:
        request: Django请求对象，包含商品ID
    Returns:
        APIResponse: 删除结果
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取商品ID
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
        
        # 检查是否是商品发布者
        if product.user_id.user_id != user.user_id:
            return APIResponse(code=1, msg='无权操作此商品')
        
        # 删除商品图片
        ProductImage.objects.filter(product_id=product).delete()
        
        # 删除商品
        product.delete()
        
        return APIResponse(code=0, msg='删除成功')
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='删除失败')


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def myList(request):
    """
    获取用户发布的商品列表接口
    Args:
        request: Django请求对象，支持分页和状态过滤
    Returns:
        APIResponse: 用户发布的商品列表
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 查询参数
        status = request.GET.get('status', None)
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        
        # 构建查询条件
        query = Q(user_id=user)
        if status:
            query &= Q(product_status=status)
        
        # 查询商品
        products = Product.objects.filter(query).order_by('-create_time')
        
        # 计算总数
        total = products.count()
        
        # 分页
        products = products[(page - 1) * size: page * size]
        
        # 序列化
        serializer = ProductSerializer(products, many=True)
        
        # 构建返回数据
        data = {
            'list': serializer.data,
            'pagination': {
                'page': page,
                'size': size,
                'total': total,
                'total_page': (total + size - 1) // size
            }
        }
        
        return APIResponse(code=0, msg='查询成功', data=data)
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='查询失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def reserve(request):
    """
    预约商品接口
    Args:
        request: Django请求对象，包含商品ID、预约时间、交易地点等信息
    Returns:
        APIResponse: 预约结果
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取商品ID
        product_id = request.data.get('product_id', None)
        if not product_id:
            return APIResponse(code=1, msg='商品ID不能为空')
        
        product = Product.objects.get(pk=product_id)
        
        # 检查商品状态
        if product.product_status != 0:
            return APIResponse(code=1, msg='该商品不可预约')
        
        # 检查是否是自己发布的商品
        if product.user_id.user_id == user.user_id:
            return APIResponse(code=1, msg='不能预约自己发布的商品')
        
        # 获取预约信息
        reserve_time = request.data.get('reserve_time', None)
        trade_location = request.data.get('trade_location', None)
        remark = request.data.get('remark', '')
        
        if not reserve_time or not trade_location:
            return APIResponse(code=1, msg='预约时间和交易地点不能为空')
        
        # 创建预约记录
        reserve_data = {
            'user_id': user,
            'product_id': product,
            'reserve_time': reserve_time,
            'trade_location': trade_location,
            'remark': remark,
            'reserve_status': 0  # 0-待确认
        }
        
        reserve = Reserve.objects.create(**reserve_data)
        
        # 更新商品状态为已预约
        product.product_status = 1  # 1-已预约
        product.save()
        
        return APIResponse(code=0, msg='预约成功', data={'reserve_id': reserve.reserve_id})
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='预约失败')