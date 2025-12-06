"""
前台公告视图模块
提供系统公告查询接口
"""
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import BNotice
from myapp.serializers import BNoticeSerializer


@api_view(['GET'])
def list_api(request):
    """
    获取公告列表接口
    Returns:
        APIResponse: 公告列表，按创建时间倒序
    """
    if request.method == 'GET':
        notices = BNotice.objects.all().order_by('-create_time')
        serializer = BNoticeSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

