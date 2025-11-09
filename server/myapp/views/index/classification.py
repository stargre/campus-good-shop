"""
前台分类视图模块
提供商品分类查询接口
"""
from django.db import connection
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Classification
from myapp.serializers import ClassificationSerializer
from myapp.utils import dict_fetchall


@api_view(['GET'])
def list_api(request):
    """
    获取分类列表接口
    Returns:
        APIResponse: 分类列表，按创建时间倒序
    """
    if request.method == 'GET':
        classifications = Classification.objects.all().order_by('-create_time')
        serializer = ClassificationSerializer(classifications, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)





