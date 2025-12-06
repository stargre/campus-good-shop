"""
后台用户管理视图模块
提供用户的CRUD操作接口
"""
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import UserInfo
from myapp.serializers import UserInfoSerializer
from myapp.utils import md5value


@api_view(['POST'])
def admin_login(request):
    """
    管理员登录接口
    """
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    
    if not username or not password:
        return APIResponse(code=1, msg='用户名或密码不能为空')
    
    # MD5加密密码
    password_md5 = md5value(password)
    
    # 查询用户
    users = User.objects.filter(username=username, password=password_md5)
    if len(users) > 0:
        user = users[0]
        
        # 检查是否为管理员账号
        if user.role not in ['0', '3']:  # 0-管理员，3-演示账号
            return APIResponse(code=1, msg='该账号不是管理员账号')
        
        # 生成AdminToken并更新用户信息
        data = {
            'admin_token': md5value(username + 'admin')  # 使用用户名+admin作为Token
        }
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user_data['admin_token'] = data['admin_token']  # 返回Token
            return APIResponse(code=0, msg='登录成功', data=user_data)
        else:
            print(serializer.errors)
    
    return APIResponse(code=1, msg='用户名或密码错误')


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """用户列表接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def info(request):
    """用户信息接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """创建用户接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """更新用户接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def updatePwd(request):
    """修改密码接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """删除用户接口 - 待实现"""
    return APIResponse(code=1, msg='功能待实现')

