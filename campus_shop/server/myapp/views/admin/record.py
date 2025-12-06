"""后台浏览记录管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """浏览记录列表接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建浏览记录接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新浏览记录接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除浏览记录接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')

