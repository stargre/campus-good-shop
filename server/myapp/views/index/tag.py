"""
前台标签视图模块
提供商品标签查询接口
"""
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Tag
from myapp.serializers import TagSerializer


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

