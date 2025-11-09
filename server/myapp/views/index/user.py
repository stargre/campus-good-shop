"""
前台用户视图模块
提供前台用户的登录、注册、信息管理等接口
"""
import datetime

from rest_framework.decorators import api_view, authentication_classes, throttle_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.auth.throttling import MyRateThrottle
from myapp.handler import APIResponse
from myapp.models import User
from myapp.serializers import UserSerializer, LoginLogSerializer
from myapp.utils import md5value


def make_login_log(request):
    """
    创建登录日志
    Args:
        request: Django请求对象
    """
    try:
        username = request.data['username']
        data = {
            "username": username,
            "ip": utils.get_ip(request),
            "ua": utils.get_ua(request)
        }
        serializer = LoginLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    except Exception as e:
        print(e)


@api_view(['POST'])
def login(request):
    """
    用户登录接口
    Args:
        request: Django请求对象，包含username和password
    Returns:
        APIResponse: 登录结果，成功返回用户信息和token
    """
    username = request.data['username']
    password = utils.md5value(request.data['password'])  # MD5加密密码

    # 查询用户
    users = User.objects.filter(username=username, password=password)
    if len(users) > 0:
        user = users[0]

        # 检查是否为后台管理员账号
        if user.role in ['1', '3']:
            return APIResponse(code=1, msg='该帐号为后台管理员帐号')

        # 生成Token并更新用户信息
        data = {
            'username': username,
            'password': password,
            'token': md5value(username)  # 使用用户名MD5作为Token
        }
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            make_login_log(request)  # 记录登录日志
            return APIResponse(code=0, msg='登录成功', data=serializer.data)
        else:
            print(serializer.errors)

    return APIResponse(code=1, msg='用户名或密码错误')


@api_view(['POST'])
@throttle_classes([MyRateThrottle])  # 限流：5次/分钟
def register(request):
    """
    用户注册接口
    Args:
        request: Django请求对象，包含username、password、repassword
    Returns:
        APIResponse: 注册结果
    """
    print(request.data)
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    repassword = request.data.get('repassword', None)
    if not username or not password or not repassword:
        return APIResponse(code=1, msg='用户名或密码不能为空')
    if password != repassword:
        return APIResponse(code=1, msg='密码不一致')
    users = User.objects.filter(username=username)
    if len(users) > 0:
        return APIResponse(code=1, msg='该用户名已存在')

    data = {
        'username': username,
        'password': password,
        'role': 2,  # 角色2
        'status': 0,
    }
    data.update({'password': utils.md5value(request.data['password'])})
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='创建失败')


@api_view(['GET'])
def info(request):
    """
    获取用户信息接口
    Args:
        request: Django请求对象，GET参数包含id
    Returns:
        APIResponse: 用户信息
    """
    if request.method == 'GET':
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])  # 需要Token认证
def update(request):
    """
    更新用户信息接口
    Args:
        request: Django请求对象，GET参数包含id，POST数据包含要更新的字段
    Returns:
        APIResponse: 更新结果
    """
    try:
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    data = request.data.copy()
    if 'username' in data.keys():
        del data['username']
    if 'password' in data.keys():
        del data['password']
    if 'role' in data.keys():
        del data['role']
    serializer = UserSerializer(user, data=data)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])  # 需要Token认证
def updatePwd(request):
    """
    修改密码接口
    Args:
        request: Django请求对象，GET参数包含id，POST数据包含password、newPassword1、newPassword2
    Returns:
        APIResponse: 修改结果
    """
    try:
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    # 验证用户角色（只能前台用户修改）
    print(user.role)
    if user.role != '2':
        return APIResponse(code=1, msg='参数非法')

    # 获取密码参数
    password = request.data.get('password', None)  # 原密码
    newPassword1 = request.data.get('newPassword1', None)  # 新密码
    newPassword2 = request.data.get('newPassword2', None)  # 确认新密码

    # 参数验证
    if not password or not newPassword1 or not newPassword2:
        return APIResponse(code=1, msg='不能为空')

    # 验证原密码
    if user.password != utils.md5value(password):
        return APIResponse(code=1, msg='原密码不正确')

    # 验证两次新密码是否一致
    if newPassword1 != newPassword2:
        return APIResponse(code=1, msg='两次密码不一致')

    # 更新密码
    data = request.data.copy()
    data.update({'password': utils.md5value(newPassword1)})  # MD5加密新密码
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='更新失败')