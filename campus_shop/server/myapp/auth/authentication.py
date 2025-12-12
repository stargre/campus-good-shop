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
            tuple: (user, None) 验证通过
        Raises:
            AuthenticationFailed: 验证失败
        """
        # 尝试多种途径获取 AdminToken（兼容不同客户端/代理）
        adminToken = None
        meta = getattr(request, 'META', {}) or {}
        # 常见直接头
        adminToken = meta.get('HTTP_ADMINTOKEN') or meta.get('HTTP_ADMIN_TOKEN')
        # Django Request.headers（DRF 提供）
        headers = getattr(request, 'headers', None)
        if not adminToken and headers:
            adminToken = headers.get('ADMINTOKEN') or headers.get('AdminToken')
        # 查询参数或GET兼容
        if not adminToken and hasattr(request, 'GET'):
            adminToken = request.GET.get('adminToken')
        # Authorization: Bearer <token>
        if not adminToken:
            auth_header = meta.get('HTTP_AUTHORIZATION') or (headers.get('Authorization') if headers else None)
            if auth_header and isinstance(auth_header, str) and auth_header.lower().startswith('bearer '):
                adminToken = auth_header[7:]

        if isinstance(adminToken, str):
            adminToken = adminToken.strip()

        print("检查adminToken==>" + str(adminToken))

        user = None
        # 优先使用 token 定位用户
        if adminToken:
            users = UserInfo.objects.filter(token=adminToken)
            if users:
                user = users[0]
            else:
                print(f'未在数据库中找到 token={adminToken!r} 对应的用户')

        # 如果没有 token，则回退到 session（登录后写入）或 header/GET 指定的用户名
        if not user:
            # session 中的管理员 id（admin_login 会写入）
            try:
                sess = getattr(request, 'session', {}) or {}
                sid = sess.get('admin_user_id') or sess.get('user_id')
                if sid:
                    try:
                        user = UserInfo.objects.get(user_id=sid)
                        print(f'通过 session 找到用户: {user.user_student_id}')
                    except Exception:
                        user = None
            except Exception:
                user = None

        if not user:
            # 支持通过请求头或查询参数提供用户名以便开发测试
            admin_user = None
            headers = getattr(request, 'headers', None)
            if headers:
                admin_user = headers.get('ADMINUSER') or headers.get('AdminUser') or headers.get('USERNAME')
            if not admin_user and hasattr(request, 'GET'):
                admin_user = request.GET.get('adminUser') or request.GET.get('username')
            if admin_user:
                try:
                    user = UserInfo.objects.get(user_student_id=admin_user)
                    print(f'通过 header/GET 找到用户: {user.user_student_id}')
                except UserInfo.DoesNotExist:
                    user = None

        # 最终判断用户与权限
        allowed_roles = ['1', '3', 'A']
        if not user:
            print('没有找到可用的管理员用户，认证失败')
            raise exceptions.AuthenticationFailed('AUTH_FAIL_END')
        if str(user.role) not in allowed_roles:
            print(f'用户角色为 {user.role}，不在允许列表 {allowed_roles} 中，拒绝访问')
            raise exceptions.AuthenticationFailed('AUTH_FAIL_END')
        if user.user_status == 0:
            print(f'用户 {user.user_student_id} 状态为禁用，user_status={user.user_status}')
            raise exceptions.AuthenticationFailed('AUTH_FAIL_END')
        print('adminToken/会话 验证通过，用户:', user.user_student_id)
        return (user, None)


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
            tuple: (user, None) 验证通过
        Raises:
            AuthenticationFailed: 验证失败
        """
        # 尝试多种途径获取前端 Token
        token = None
        meta = getattr(request, 'META', {}) or {}
        token = meta.get('HTTP_TOKEN') or meta.get('HTTP_AUTH_TOKEN')
        headers = getattr(request, 'headers', None)
        if not token and headers:
            token = headers.get('TOKEN') or headers.get('Token')
        if not token and hasattr(request, 'GET'):
            token = request.GET.get('token') or request.GET.get('Token')
        if not token:
            auth_header = meta.get('HTTP_AUTHORIZATION') or (headers.get('Authorization') if headers else None)
            if auth_header and isinstance(auth_header, str) and auth_header.lower().startswith('bearer '):
                token = auth_header[7:]

        if isinstance(token, str):
            token = token.strip()

        if token:
            print("检查token==>" + str(token))
            users = UserInfo.objects.filter(token=token)
            # 验证逻辑：只允许普通用户(role='2')，拒绝管理员(role='1','3')
            if len(users) == 0 or (users[0].role in ['1', '3']):
                print(f'未找到普通用户或角色不符合，token={token!r}')
                raise exceptions.AuthenticationFailed("AUTH_FAIL_FRONT")
            else:
                user = users[0]
                # 检查用户状态
                if user.user_status == 0:
                    print(f'用户 {user.user_student_id} 状态为禁用，user_status={user.user_status}')
                    raise exceptions.AuthenticationFailed("AUTH_FAIL_FRONT")
                print('token验证通过')
                return (user, None)  # 重要：必须返回(user, None)
        else:
            print("检查token==>token 为空")
            raise exceptions.AuthenticationFailed("AUTH_FAIL_FRONT")