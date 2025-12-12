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
    try:
        # 获取查询参数
        category_id = request.GET.get('category_id', None)
        keyword = request.GET.get('keyword', None)
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        try:
            page_size = int(request.GET.get('page_size', 10))
        except (ValueError, TypeError):
            page_size = 10

        # 基础查询集
        products = Product.objects.all()

        # 分类过滤
        if category_id:
            try:
                products = products.filter(category_id=int(category_id))
            except (ValueError, TypeError):
                pass

        # 关键词搜索
        if keyword:
            products = products.filter(product_title__contains=keyword)

        # 总数
        total = products.count()

        # 分页（按创建时间倒序）
        start = (page - 1) * page_size
        end = start + page_size
        products = products.order_by('-create_time')[start:end]

        # 序列化
        serializer = ProductSerializer(products, many=True)

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
    """商品详情接口"""
    try:
        pk = request.GET.get('id', -1)
        product = Product.objects.get(pk=pk)
        
        # 序列化
        serializer = ProductDetailSerializer(product)
        
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建商品接口 - 移除Tag相关代码"""
    data = request.data.copy()
    
    # 移除Tag相关代码
    # tag_ids = data.pop('tags', [])  # 删除这行
    
    # 处理category_id和category字段的映射
    if 'category_id' in data:
        data['category'] = data.pop('category_id')
    
    # 序列化验证
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        # 保存商品
        product = serializer.save()
        
        # 移除Tag相关代码
        # if tag_ids:
        #     tags = Tag.objects.filter(id__in=tag_ids)
        #     product.tags.set(tags)
        
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print("Serializer errors:", serializer.errors)
        return APIResponse(code=1, msg='参数错误', data=serializer.errors)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新商品接口 - 移除Tag相关代码"""
    try:
        # 同时从请求体和URL参数中获取商品ID
        pk_str = request.data.get('id') or request.data.get('product_id') or request.GET.get('id') or request.GET.get('product_id')
        
        if not pk_str:
            return APIResponse(code=1, msg='商品ID不能为空')
        
        # 转换为整数
        pk = int(pk_str)
        product = Product.objects.get(pk=pk)
        
        data = request.data.copy()
        # 处理category_id和category字段的映射，确保可以更新分类
        if 'category_id' in data:
            cid = data.get('category_id')
            cid_str = str(cid).strip() if cid is not None else ''
            if cid_str == '':
                # 空值则不更新分类，移除该字段避免类型转换错误
                data.pop('category_id', None)
            else:
                try:
                    data['category'] = int(cid_str)
                    data.pop('category_id', None)
                except (ValueError, TypeError):
                    return APIResponse(code=1, msg='分类ID格式不正确')
        
        # 序列化验证 - 让序列化器处理必填字段验证
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            # 保存更新
            product = serializer.save()
            
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except ValueError as e:
        return APIResponse(code=1, msg='商品ID格式错误，必须是数字')
    except Exception as e:
        return APIResponse(code=1, msg='更新失败，请稍后重试')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除商品接口"""
    try:
        # 同时从请求体和URL参数中获取商品ID
        pk_str = request.data.get('id') or request.data.get('product_id') or request.GET.get('id') or request.GET.get('product_id')
        
        if not pk_str:
            return APIResponse(code=1, msg='商品ID不能为空')
        
        # 转换为整数
        pk = int(pk_str)
        product = Product.objects.get(pk=pk)
        
        # 删除商品
        product.delete()
        
        return APIResponse(code=0, msg='删除成功')
        
    except ValueError as e:
        return APIResponse(code=1, msg='商品ID格式错误，必须是数字')
    except Product.DoesNotExist:
        return APIResponse(code=1, msg='商品不存在')
    except Exception as e:
        return APIResponse(code=1, msg='删除失败，请稍后重试')
