"""
后台订单管理视图模块
"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """订单列表接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建订单接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新订单接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def cancel_order(request):
    """取消订单接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delay(request):
    """延期订单接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除订单接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')

@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def detail(request):
    """订单详情接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')
