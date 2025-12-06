"""
前台分类视图模块
提供商品分类查询接口
"""
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Category
from myapp.serializers import CategorySerializer


@api_view(['GET'])
def list_api(request):
    """
    获取标签列表接口
    Returns:
        APIResponse: 标签列表，按创建时间倒序
    """
    if request.method == 'GET':
        categorys = Category.objects.all().order_by('-create_time')
        serializer = CategorySerializer(categorys, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

from django.shortcuts import get_object_or_404

@api_view(['GET'])
def detail(request):
    """
    获取单个标签详情接口
    查询参数: id（标签ID）
    """
    category_id = request.GET.get('id')
    if not category_id:
        return APIResponse(code=1, msg='缺少分类ID')

    category = get_object_or_404(Category, id=category_id)
    serializer = CategorySerializer(category)
    return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def listWithProducts(request):
    """
    获取所有分类及其关联的商品列表
    """
    from myapp.models import Product
    from myapp.serializers import ProductSerializer
    
    categories = Category.objects.all().order_by('-category_create_time')
    result = []
    for category in categories:
        products = Product.objects.filter(category=category, product_status=1).order_by('-create_time')[:10]
        products_data = ProductSerializer(products, many=True).data
        result.append({
            'category_id': category.category_id,
            'category_name': category.category_name,
            'category_create_time': category.category_create_time,
            'products': products_data
        })
    return APIResponse(code=0, msg='查询成功', data=result)