"""后台分类管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Category
from myapp.serializers import CategorySerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """分类列表接口"""
    try:
        categories = Category.objects.all().order_by('category_sort_order')
        serializer = CategorySerializer(categories, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建分类接口"""
    try:
        data = request.data.copy()
        
        # 验证必填字段
        if not data.get('category_name'):
            return APIResponse(code=1, msg='分类名称不能为空')
        
        # 检查分类名是否重复
        if Category.objects.filter(category_name=data['category_name']).exists():
            return APIResponse(code=1, msg='分类名称已存在')
        
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
    except Exception as e:
        return APIResponse(code=1, msg=f'创建失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新分类接口"""
    try:
        # 同时从请求体和URL参数中获取分类ID
        category_id = request.data.get('category_id') or request.GET.get('category_id')
        if not category_id:
            return APIResponse(code=1, msg='分类ID不能为空')
        
        category = Category.objects.get(category_id=category_id)
        data = request.data.copy()
        
        # 检查分类名是否重复（排除自己）
        if 'category_name' in data and data['category_name'] != category.category_name:
            if Category.objects.filter(category_name=data['category_name']).exclude(category_id=category_id).exists():
                return APIResponse(code=1, msg='分类名称已存在')
        
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
    except Category.DoesNotExist:
        return APIResponse(code=1, msg='分类不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'更新失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除分类接口（支持单个删除和批量删除）"""
    try:
        # 支持单个删除和批量删除
        # 单个删除：从请求体或URL参数中获取category_id或id
        # 批量删除：从请求体或URL参数中获取ids（逗号分隔的ID列表）
        category_id = request.data.get('category_id') or request.GET.get('category_id') or request.data.get('id') or request.GET.get('id')
        ids = request.data.get('ids') or request.GET.get('ids')
        
        if not category_id and not ids:
            return APIResponse(code=1, msg='分类ID不能为空')
        
        # 检查是否有商品使用该分类
        from myapp.models import Product
        
        # 处理单个删除
        if category_id:
            if Product.objects.filter(category_id=category_id).exists():
                return APIResponse(code=1, msg='该分类下还有商品，不能删除')
            
            category = Category.objects.get(category_id=category_id)
            category.delete()
        # 处理批量删除
        elif ids:
            category_ids = ids.split(',')
            for cid in category_ids:
                if Product.objects.filter(category_id=cid).exists():
                    return APIResponse(code=1, msg=f'分类ID {cid} 下还有商品，不能删除')
            
            Category.objects.filter(category_id__in=category_ids).delete()
        
        return APIResponse(code=0, msg='删除成功')
    except Category.DoesNotExist:
        return APIResponse(code=1, msg='分类不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')