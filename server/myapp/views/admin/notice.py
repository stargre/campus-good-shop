"""后台公告管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from django.db import models
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import BNotice
from myapp.serializers import BNoticeSerializer


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """公告列表接口"""
    try:
        # 获取查询参数
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 基础查询集
        notices = BNotice.objects.all()
        
        # 关键词搜索
        if keyword:
            notices = notices.filter(notice_content__contains=keyword)
        
        # 总数
        total = notices.count()
        
        # 分页（按排序值和创建时间）
        start = (page - 1) * page_size
        end = start + page_size
        notices = notices.order_by('sort_value', '-create_time')[start:end]
        
        # 序列化
        serializer = BNoticeSerializer(notices, many=True)
        
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建公告接口"""
    try:
        data = request.data.copy()
        
        # 验证必填字段
        if not data.get('notice_content'):
            return APIResponse(code=1, msg='公告内容不能为空')
        
        # 设置默认排序值
        if 'sort_value' not in data or data['sort_value'] == '':
            # 获取最大排序值+10
            max_sort = BNotice.objects.aggregate(max_sort=models.Max('sort_value'))['max_sort'] or 0
            data['sort_value'] = max_sort + 10
        
        serializer = BNoticeSerializer(data=data)
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
    """更新公告接口"""
    try:
        notice_id = request.data.get('b_notice_id') or request.GET.get('b_notice_id') or request.data.get('id') or request.GET.get('id')
        if not notice_id:
            return APIResponse(code=1, msg='公告ID不能为空')
        
        notice = BNotice.objects.get(b_notice_id=notice_id)
        data = request.data.copy()
        
        serializer = BNoticeSerializer(notice, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
    except BNotice.DoesNotExist:
        return APIResponse(code=1, msg='公告不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'更新失败: {str(e)}')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除公告接口"""
    try:
        notice_id = request.data.get('b_notice_id') or request.GET.get('b_notice_id') or request.data.get('id') or request.GET.get('id')
        ids = request.data.get('ids') or request.GET.get('ids')
        if not notice_id and not ids:
            return APIResponse(code=1, msg='公告ID不能为空')
        
        if ids:
            id_list = [int(x) for x in str(ids).split(',') if x]
            BNotice.objects.filter(b_notice_id__in=id_list).delete()
        else:
            notice = BNotice.objects.get(b_notice_id=notice_id)
            notice.delete()
        
        return APIResponse(code=0, msg='删除成功')
    except BNotice.DoesNotExist:
        return APIResponse(code=1, msg='公告不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')
