"""
前台商品视图模块
提供商品列表、详情、收藏、心愿单等接口
"""
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.handler import APIResponse
from myapp.models import Category, Product, Tag, UserInfo
from myapp.serializers import ProductSerializer, CategorySerializer, ListProductSerializer, ProductDetailSerializer
from myapp.utils import dict_fetchall


@api_view(['GET'])
def list_api(request):
    """
    商品列表接口
    支持按关键词、分类、标签筛选，支持按时间、热度排序
    Args:
        request: Django请求对象，GET参数包含keyword、c（分类）、tag、sort（排序方式）
    Returns:
        APIResponse: 商品列表
    """
    if request.method == 'GET':
        keyword = request.GET.get("keyword", None)
        c = request.GET.get("c", None)
        tag = request.GET.get("tag", None)
        sort = request.GET.get("sort", 'recent')

        # 排序方式
        order = '-create_time'
        if sort == 'recent':
            order = '-create_time'
        elif sort == 'hot' or sort == 'recommend':
            order = '-pv'

        if keyword:
            things = Product.objects.filter(title__contains=keyword).order_by(order)

        # todo
        elif c and int(c) > -1:
            ids = [c]

            things = Product.objects.filter(category_id__in=ids).order_by(order)

        elif tag:
            tag = Tag.objects.get(id=tag)
            print(tag)
            things = tag.product_set.all().order_by(order)
        else:
            things = Product.objects.all().order_by(order)

        serializer = ListProductSerializer(things, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def detail(request):
    """
    商品详情接口
    Args:
        request: Django请求对象，GET参数包含id
    Returns:
        APIResponse: 商品详情信息
    """
    try:
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        utils.log_error(request, '对象不存在')  # 记录错误日志
        return APIResponse(code=1, msg='对象不存在')

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def increaseWishCount(request):
    """
    增加心愿单数量接口
    Args:
        request: Django请求对象，GET参数包含id
    Returns:
        APIResponse: 操作结果
    """
    try:
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
        # 心愿单数量加1
        thing.wish_count = thing.wish_count + 1
        thing.save()
    except Product.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    serializer = ProductSerializer(product)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)

@api_view(['POST'])
def increaseRecommendCount(request):
    try:
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
        # recommend_count加1
        thing.recommend_count = thing.recommend_count + 1
        thing.save()
    except Product.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    serializer = ProductSerializer(product)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)

@api_view(['POST'])
def addWishUser(request):
    """
    添加用户到心愿单接口
    Args:
        request: Django请求对象，GET参数包含username和thingId
    Returns:
        APIResponse: 操作结果
    """
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = UserInfo.objects.get(username=username)
            product = Product.objects.get(pk=thingId)

            # 如果用户不在心愿单中，则添加
            # 使用新的数据模型关系
            from myapp.models import ProductWish
            # 检查是否已存在心愿单记录
            if not ProductWish.objects.filter(user=user, product=product).exists():
                ProductWish.objects.create(user=user, product=product)

    except Product.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    serializer = ProductSerializer(product)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)

@api_view(['POST'])
def removeWishUser(request):
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = UserInfo.objects.get(username=username)
            product = Product.objects.get(pk=thingId)

            # 使用新的数据模型关系
            from myapp.models import ProductWish
            # 删除心愿单记录
            ProductWish.objects.filter(user=user, product=product).delete()

    except Product.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功')

@api_view(['GET'])
def getWishThingList(request):
    try:
        username = request.GET.get('username', None)
        if username:
            user = UserInfo.objects.get(username=username)
            # 使用新的数据模型关系
            from myapp.models import ProductWish
            wish_products = ProductWish.objects.filter(user=user).values_list('product_id', flat=True)
            things = Product.objects.filter(id__in=wish_products)
            serializer = ListProductSerializer(things, many=True)
            return APIResponse(code=0, msg='操作成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='username不能为空')

    except Exception as e:
        utils.log_error(request, '操作失败' + str(e))
        return APIResponse(code=1, msg='获取心愿单失败')


@api_view(['POST'])
def addCollectUser(request):
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = UserInfo.objects.get(username=username)
            product = Product.objects.get(pk=thingId)

            # 使用新的数据模型关系
            from myapp.models import ProductCollection
            # 检查是否已存在收藏记录
            if not ProductCollection.objects.filter(user=user, product=product).exists():
                ProductCollection.objects.create(user=user, product=product)

    except Product.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    serializer = DetailProductSerializer(product)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)


@api_view(['POST'])
def removeCollectUser(request):
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = UserInfo.objects.get(username=username)
            product = Product.objects.get(pk=thingId)

            # 使用新的数据模型关系
            from myapp.models import ProductCollection
            # 删除收藏记录
            ProductCollection.objects.filter(user=user, product=product).delete()

    except Product.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功')


@api_view(['GET'])
def getCollectThingList(request):
    try:
        username = request.GET.get('username', None)
        if username:
            user = UserInfo.objects.get(username=username)
            # 使用新的数据模型关系
            from myapp.models import ProductCollection
            collect_products = ProductCollection.objects.filter(user=user).values_list('product_id', flat=True)
            things = Product.objects.filter(id__in=collect_products)
            serializer = ListProductSerializer(things, many=True)
            return APIResponse(code=0, msg='操作成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='username不能为空')

    except Exception as e:
        utils.log_error(request, '操作失败' + str(e))
        return APIResponse(code=1, msg='获取收藏失败')


