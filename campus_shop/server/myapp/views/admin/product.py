"""
后台商品管理视图模块
提供商品的CRUD操作接口
"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Product, Category
from myapp.serializers import ProductSerializer, ProductDetailSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """商品列表接口"""
    # 获取查询参数
    category_id = request.GET.get('category_id', None)
    keyword = request.GET.get('keyword', None)
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    # 基础查询集
    products = Product.objects.all()
    
    # 分类过滤
    if category_id:
        products = products.filter(category_id=category_id)
    
    # 关键词搜索
    if keyword:
        products = products.filter(title__contains=keyword)
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    products = products[start:end]
    
    # 序列化
    serializer = ProductSerializer(products, many=True)
    
    return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def detail(request):
    """商品详情接口"""
    try:
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
        
        # 序列化
        serializer = DetailProductSerializer(product)
        
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建商品接口"""
    data = request.data.copy()
    
    # 处理标签
    tag_ids = data.pop('tags', [])
    
    # 序列化验证
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        # 保存商品
        product = serializer.save()
        
        # 添加标签关联
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            product.tags.set(tags)
        
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        return APIResponse(code=1, msg='参数错误', data=serializer.errors)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新商品接口"""
    try:
        pk = request.POST.get('id', -1)
        product = Product.objects.get(pk=pk)
        
        data = request.data.copy()
        # 处理标签
        tag_ids = data.pop('tags', [])
        
        # 序列化验证
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            # 保存更新
            product = serializer.save()
            
            # 更新标签关联
            if tag_ids:
                tags = Tag.objects.filter(id__in=tag_ids)
                product.tags.set(tags)
            
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除商品接口"""
    try:
        pk = request.POST.get('id', -1)
        product = Product.objects.get(pk=pk)
        
        # 删除商品
        product.delete()
        
        return APIResponse(code=0, msg='删除成功')
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')

