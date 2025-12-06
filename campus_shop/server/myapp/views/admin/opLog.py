"""后台操作日志管理视图模块"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """操作日志列表接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')

