"""
前台分类视图模块
实现商品分类的查询和展示功能
"""
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from myapp.handler import APIResponse
from myapp.models import Category
from myapp.serializers import CategorySerializer


@api_view(['GET'])
def list(request):
    """
    获取分类列表接口
    Args:
        request: Django请求对象
    Returns:
        APIResponse: 分类列表数据
    """
    try:
        # 查询所有分类
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='查询失败')


@api_view(['GET'])
def detail(request):
    """
    获取单个分类详情接口
    Args:
        request: Django请求对象，包含分类ID参数
    Returns:
        APIResponse: 分类详情数据
    """
    try:
        pk = request.GET.get('id', -1)
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Category.DoesNotExist:
        return APIResponse(code=1, msg='分类不存在')
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='查询失败')


@api_view(['GET'])
def listWithProducts(request):
    """
    获取分类列表及其商品数量接口
    Args:
        request: Django请求对象
    Returns:
        APIResponse: 带商品数量的分类列表
    """
    try:
        categories = Category.objects.all()
        categories_data = []
        
        for category in categories:
            # 获取分类下的商品数量
            product_count = category.product_set.count()
            category_dict = CategorySerializer(category).data
            category_dict['product_count'] = product_count
            categories_data.append(category_dict)
        
        return APIResponse(code=0, msg='查询成功', data=categories_data)
    except Exception as e:
        print(e)
        return APIResponse(code=1, msg='查询失败')





