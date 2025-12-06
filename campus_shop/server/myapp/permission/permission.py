"""
权限检查模块
提供权限相关的检查函数
"""
from myapp.models import UserInfo


def isDemoAdminUser(request):
    """
    检查是否为演示管理员账号
    Args:
        request: Django请求对象
    Returns:
        bool: 如果是演示账号返回True，否则返回False
    """
    adminToken = request.META.get("HTTP_ADMINTOKEN")
    users = UserInfo.objects.filter(admin_token=adminToken)
    if len(users) > 0:
        user = users[0]
        if user.role == '3':  # 角色3表示演示账号
            print('演示帐号===>')
            return True
    return False
