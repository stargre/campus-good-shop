"""
前台搜索视图模块
提供商品搜索功能接口
"""
from rest_framework.decorators import api_view
from django.db.models import Q

from myapp.handler import APIResponse
from myapp.models import Product
from myapp.serializers import ProductSerializer


@api_view(['GET'])
def search(request):
    """
    搜索商品接口
    查询参数:
        keyword: 搜索关键词
        category_id: 分类ID（可选）
        min_price: 最低价格（可选，单位：元）
        max_price: 最高价格（可选，单位：元）
        page: 页码，默认1
        page_size: 每页数量，默认10
    Returns:
        APIResponse: 搜索结果列表和分页信息
    """
    if request.method == 'GET':
        # 获取查询参数
        keyword = request.GET.get('keyword', '')
        category_id = request.GET.get('category_id', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 构建查询
        query = Q(product_status=1)
        
        if keyword:
            query &= Q(product_title__icontains=keyword) | Q(content__icontains=keyword)
        
        if category_id:
            query &= Q(category_id=category_id)
        
        if min_price:
            try:
                # 将元转换为分
                query &= Q(product_price__gte=int(float(min_price) * 100))
            except ValueError:
                pass
        
        if max_price:
            try:
                # 将元转换为分
                query &= Q(product_price__lte=int(float(max_price) * 100))
            except ValueError:
                pass
        
        # 执行查询并分页
        products = Product.objects.filter(query).order_by('-create_time')
        
        # 计算分页
        total = products.count()
        start = (page - 1) * page_size
        end = start + page_size
        page_products = products[start:end]
        
        # 序列化
        serializer = ProductSerializer(page_products, many=True)
        
        # 返回结果
        return APIResponse(
            code=0,
            msg='搜索成功',
            data={
                'list': serializer.data,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_page': (total + page_size - 1) // page_size
            }
        )


@api_view(['GET'])
def hotKeywords(request):
    """
    获取热门搜索关键词
    Returns:
        APIResponse: 热门关键词列表
    """
    if request.method == 'GET':
        # 这里可以从数据库或者配置文件中获取热门关键词
        # 暂时返回一些示例数据
        hot_keywords = [
            '考研资料', '教材', '笔记本电脑', '篮球', '自行车',
            '充电宝', '耳机', 'U盘', '书籍', '文具'
        ]
        return APIResponse(code=0, msg='获取成功', data=hot_keywords)