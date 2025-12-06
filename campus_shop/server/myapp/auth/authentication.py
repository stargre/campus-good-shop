"""
身份认证模块
提供后台管理员和前台用户的Token认证
"""
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from myapp.models import UserInfo


class AdminTokenAuthtication(BaseAuthentication):
    """
    后台管理员Token认证类
    用于后台管理接口的身份验证
    """
    def authenticate(self, request):
        """
        验证后台管理员Token
        Args:
            request: Django请求对象
        Returns:
            None: 验证通过
        Raises:
            AuthenticationFailed: 验证失败
        """
        # 从请求头获取AdminToken
        adminToken = request.META.get("HTTP_ADMINTOKEN")
        print("检查adminToken==>" + adminToken)
        users = UserInfo.objects.filter(admin_token=adminToken)
        """
        判定条件：
            1. 传了adminToken 
            2. 查到了该帐号 
            3. 该帐号是管理员（role='0'）或演示帐号（role='3'）
        """
        if not adminToken or len(users) == 0 or users[0].role == '2':
            raise exceptions.AuthenticationFailed("AUTH_FAIL_END")
        else:
            print('adminToken验证通过')


class TokenAuthtication(BaseAuthentication):
    """
    前台用户Token认证类
    用于前台用户接口的身份验证
    """
    def authenticate(self, request):
        """
        验证前台用户Token
        Args:
            request: Django请求对象
        Returns:
            None: 验证通过
        Raises:
            AuthenticationFailed: 验证失败
        """
        # 从请求头获取Token
        token = request.META.get("HTTP_TOKEN", "")
        if token is not None:
            print("检查token==>" + token)
            users = UserInfo.objects.filter(token=token)
            """
            判定条件：
                1. 传了token 
                2. 查到了该帐号 
                3. 该帐号是前台用户（role='2'），不能是管理员（role='1'）或演示账号（role='3'）
            """
            if not token or len(users) == 0 or (users[0].role in ['1', '3']):
                raise exceptions.AuthenticationFailed("AUTH_FAIL_FRONT")
            else:
                print('token验证通过')
        else:
            print("检查token==>token 为空")
            raise exceptions.AuthenticationFailed("AUTH_FAIL_FRONT")
