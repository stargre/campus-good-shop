"""
后台总览视图模块
提供数据统计和系统信息接口
"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def count(request):
    """
    获取数据统计接口
    注意：此函数需要根据实际需求实现
    """
    # TODO: 实现数据统计逻辑
    return APIResponse(code=1, msg='功能待实现')


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def sysInfo(request):
    """
    获取系统信息接口
    注意：此函数需要根据实际需求实现
    """
    # TODO: 实现系统信息获取逻辑
    return APIResponse(code=1, msg='功能待实现')

