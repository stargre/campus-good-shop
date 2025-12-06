"""
前台标签视图模块
提供商品标签查询接口
"""
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from myapp.handler import APIResponse
from myapp.models import Tag, Product
from myapp.serializers import TagSerializer, ProductSerializer


@api_view(['GET'])
def list_api(request):
    """
    获取标签列表接口
    Returns:
        APIResponse: 标签列表，按创建时间倒序
    """
    if request.method == 'GET':
        tags = Tag.objects.all().order_by('-create_time')
        serializer = TagSerializer(tags, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def detail(request):
    """
    获取单个标签详情接口
    查询参数: tag_id（标签ID）
    """
    tag_id = request.GET.get('tag_id')
    if not tag_id:
        return APIResponse(code=1, msg='缺少标签ID')

    tag = get_object_or_404(Tag, tag_id=tag_id)
    serializer = TagSerializer(tag)
    return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def listWithProducts(request):
    """
    获取所有标签及其关联的商品列表
    """
    tags = Tag.objects.all().order_by('-create_time')
    result = []
    for tag in tags:
        # 获取与标签关联的商品（通过ProductTag中间表）
        products = Product.objects.filter(
            producttag__tag_id=tag, 
            product_status=1
        ).order_by('-create_time')[:10]
        products_data = ProductSerializer(products, many=True).data
        result.append({
            'tag_id': tag.tag_id,
            'tag_name': tag.tag_name,
            'create_time': tag.create_time,
            'products': products_data
        })
    return APIResponse(code=0, msg='查询成功', data=result)