"""后台轮播图管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from django.db import models
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Banner
from myapp.serializers import BannerSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """轮播图列表接口"""
    try:
        # 获取查询参数
        keyword = request.GET.get('keyword', '')
        status = request.GET.get('status', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 基础查询集
        banners = Banner.objects.all()
        
        # 关键词搜索
        if keyword:
            banners = banners.filter(
                Q(title__contains=keyword) |
                Q(description__contains=keyword) |
                Q(url__contains=keyword)
            )
        
        # 状态筛选
        if status:
            banners = banners.filter(status=int(status))
        
        # 总数
        total = banners.count()
        
        # 分页（按排序值和创建时间）
        start = (page - 1) * page_size
        end = start + page_size
        banners = banners.order_by('sort_order', '-create_time')[start:end]
        
        # 序列化
        serializer = BannerSerializer(banners, many=True)
        
        return APIResponse(code=0, msg='查询成功', data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_page': (total + page_size - 1) // page_size
        })
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建轮播图接口"""
    try:
        data = request.data.copy()
        
        # 验证必填字段
        required_fields = ['title', 'image_url', 'url']
        for field in required_fields:
            if not data.get(field):
                return APIResponse(code=1, msg=f'{field}不能为空')
        
        # 设置默认值
        if 'sort_order' not in data or data['sort_order'] == '':
            # 获取最大排序值+10
            max_sort = Banner.objects.aggregate(max_sort=models.Max('sort_order'))['max_sort'] or 0
            data['sort_order'] = max_sort + 10
        
        if 'status' not in data:
            data['status'] = 1  # 默认启用
        
        serializer = BannerSerializer(data=data)
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
    """更新轮播图接口"""
    try:
        banner_id = request.data.get('banner_id')
        if not banner_id:
            return APIResponse(code=1, msg='轮播图ID不能为空')
        
        banner = Banner.objects.get(banner_id=banner_id)
        data = request.data.copy()
        
        serializer = BannerSerializer(banner, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
    except Banner.DoesNotExist:
        return APIResponse(code=1, msg='轮播图不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'更新失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除轮播图接口"""
    try:
        banner_id = request.data.get('banner_id')
        if not banner_id:
            return APIResponse(code=1, msg='轮播图ID不能为空')
        
        banner = Banner.objects.get(banner_id=banner_id)
        banner.delete()
        
        return APIResponse(code=0, msg='删除成功')
    except Banner.DoesNotExist:
        return APIResponse(code=1, msg='轮播图不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')