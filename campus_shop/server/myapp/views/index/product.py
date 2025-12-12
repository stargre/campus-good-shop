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
from myapp.models import Product, ProductImage, UserInfo, Reserve, Record, Address


@api_view(['GET'])
def list(request):
    """
    获取商品列表接口
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
        sort = request.GET.get('sort', 'create_time')
        order = request.GET.get('order', 'desc')
        
        # 修复：将前端排序别名映射到数据库字段
        sort_mapping = {
            'hot': 'view_count',
            'recommend': 'collect_count',
            'recent': 'create_time'
        }
        if sort in sort_mapping:
            sort = sort_mapping[sort]
        
        # 构建查询条件 - 修复字段名
        query = Q()
        if category_id:
            try:
                query &= Q(category=int(category_id))
            except (ValueError, TypeError):
                pass
        if keyword:
            # 修复：使用 content 而不是 product_desc
            query &= (Q(product_title__contains=keyword) | Q(content__contains=keyword))
        if min_price:
            query &= Q(product_price__gte=int(min_price))
        if max_price:
            query &= Q(product_price__lte=int(max_price))
        if quality:
            try:
                query &= Q(quality=int(quality))
            except (ValueError, TypeError):
                pass
        if status:
            try:
                query &= Q(product_status=int(status))
            except (ValueError, TypeError):
                pass
        
        # 应用查询条件
        products = Product.objects.filter(query)
        
        # 应用排序 - 映射前端抽象排序字段到实际数据库字段
        # 将前端的 'hot', 'recommend', 'recent' 映射到实际字段
        sort_field_map = {
            'hot': 'view_count',         # 热门 -> 浏览量
            'recommend': 'collect_count', # 推荐 -> 收藏量
            'recent': 'create_time'       # 最新 -> 创建时间
        }
        
        # 获取实际排序字段，如果不在映射中则直接使用前端传递的值
        actual_sort = sort_field_map.get(sort, sort)
        
        # 构建排序字符串
        order_by = actual_sort
        if order == 'desc':
            order_by = f'-{actual_sort}'
        
        # 应用排序
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
                            create_time=datetime.now()
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
        
        # 处理category_id和category字段的映射
        if 'category_id' in data:
            data['category'] = data.pop('category_id')
        
        # 将价格从元转换为分（整数存储）
        # 保持数据库使用的价格单位与前端一致（元，整数），不再做乘以100的转换
        for price_field in ['product_price', 'product_o_price']:
            if price_field in data and data[price_field]:
                try:
                    data[price_field] = int(float(data[price_field]))
                except (ValueError, TypeError):
                    return APIResponse(code=1, msg=f'{price_field}价格格式不正确')
        
        # 创建商品
        serializer = ProductDetailSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            
            # 处理商品图片
            if 'images' in data:
                try:
                    # 尝试解析JSON格式的图片列表
                    if isinstance(data['images'], str):
                        images = json.loads(data['images'])
                    else:
                        images = data['images']
                    images = [s for s in images if s]
                    # 入库图片列表，并记录第一张图片ID为主图ID
                    first_image_id = None
                    for idx, img_url in enumerate(images):
                        pi = ProductImage.objects.create(
                            product_id=product,
                            image_url=img_url,
                            sort_order=idx
                        )
                        if idx == 0:
                            first_image_id = pi.image_id
                    if first_image_id:
                        product.cover_image_id = first_image_id
                        product.save(update_fields=['cover_image_id'])
                except json.JSONDecodeError:
                    print("图片列表解析失败，使用空列表")
            
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        else:
            print("Serializer errors:", serializer.errors)
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
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
        
        # 获取商品ID（支持从GET或POST体中获取）
        pk = request.GET.get('id', None) or request.data.get('id', None)
        product = Product.objects.get(pk=pk)
        
        # 检查是否是商品发布者
        if product.user_id.user_id != user.user_id:
            return APIResponse(code=1, msg='无权操作此商品')
        
        # 处理价格转换与字段映射
        data = request.data.copy()
        # 字段别名映射，兼容前端表单字段
        if 'category_id' in data:
            data['category'] = data.pop('category_id')
        if 'title' in data:
            data['product_title'] = data.pop('title')
        if 'price' in data:
            data['product_price'] = data.pop('price')
        if 'description' in data:
            data['content'] = data.pop('description')
        if 'status' in data:
            data['product_status'] = data.pop('status')
        if 'product_price' in data and data['product_price']:
            try:
                data['product_price'] = int(float(data['product_price']))
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
                images = json.loads(data['images']) if isinstance(data['images'], str) else data['images']
                images = [s for s in images if s]
                product_cover_updates = {}
                first_image_id = None
                for idx, img_url in enumerate(images):
                    pi = ProductImage.objects.create(
                        product_id=product,
                        image_url=img_url,
                        sort_order=idx
                    )
                    if idx == 0:
                        first_image_id = pi.image_id
                if first_image_id:
                    product_cover_updates['cover_image_id'] = first_image_id
                if product_cover_updates:
                    Product.objects.filter(pk=product.product_id).update(**product_cover_updates)
            
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
    预约商品接口 - 修复版
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
        
        # 检查商品是否已被预约
        if product.is_reserved:
            return APIResponse(code=1, msg='该商品已被预约')
        
        # 检查商品状态（允许状态为1：审核通过的商品被预约）
        if product.product_status != 1:
            return APIResponse(code=1, msg='该商品不可预约')
        
        # 检查是否是自己发布的商品
        if product.user_id.user_id == user.user_id:
            return APIResponse(code=1, msg='不能预约自己发布的商品')
        
        # 获取预约信息
        reserve_time = request.data.get('reserve_time', None)
        trade_location = request.data.get('trade_location', None)
        remark = request.data.get('remark', '')
        address_id = request.data.get('address_id', None)
        
        if not reserve_time or not trade_location:
            return APIResponse(code=1, msg='预约时间和交易地点不能为空')
        
        # 获取卖家信息
        seller = product.user_id
        
        # 处理地址
        address = None
        if address_id:
            try:
                address = Address.objects.get(address_id=address_id, user_id=user.user_id)
            except Address.DoesNotExist:
                return APIResponse(code=1, msg='地址不存在')
        
        # 创建预约记录 - 使用新字段
        reserve_data = {
            'product_id': product,
            'user_id': user,
            'seller_id': seller,
            'reserve_time': reserve_time,
            'trade_location': trade_location,
            'remark': remark,
            'address_id': address,
            'order_id': None,  # 预约时还没有订单
            'reserve_status': 0  # 0-待确认
        }
        
        reserve = Reserve.objects.create(**reserve_data)
        
        # 更新商品的预约状态
        product.is_reserved = True
        product.save()
        
        return APIResponse(code=0, msg='预约成功', data={'reserve_id': reserve.reserve_id})
        
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        print(f"预约异常: {str(e)}")
        return APIResponse(code=1, msg='预约失败')
    
@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def cancel_reserve(request):
    """
    取消预约商品接口
    Args:
        request: Django请求对象，包含预约ID等信息
    Returns:
        APIResponse: 取消预约结果
    """
    try:
        # 获取当前登录用户
        token = request.META.get("HTTP_TOKEN", "")
        users = UserInfo.objects.filter(token=token)
        if len(users) == 0:
            return APIResponse(code=1, msg='用户未登录')
        user = users[0]
        
        # 获取预约ID
        reserve_id = request.data.get('reserve_id')
        if not reserve_id:
            return APIResponse(code=1, msg='缺少预约ID')
        
        # 查询预约记录
        try:
            reserve = Reserve.objects.get(reserve_id=reserve_id, user_id=user.user_id)
        except Reserve.DoesNotExist:
            return APIResponse(code=1, msg='预约记录不存在')
        
        # 检查预约状态（只能取消待确认的预约）
        if reserve.reserve_status != 0:
            return APIResponse(code=1, msg='只能取消待确认的预约')
        
        # 更新预约状态为已取消
        reserve.reserve_status = 3  # 3-已取消
        reserve.finish_time = datetime.datetime.now()
        reserve.save()
        
        # 更新商品的预约状态
        product = reserve.product_id
        product.is_reserved = False
        product.save()
        
        return APIResponse(code=0, msg='取消预约成功')
        
    except Exception as e:
        print(f"取消预约异常: {str(e)}")
        return APIResponse(code=1, msg='取消预约失败')
