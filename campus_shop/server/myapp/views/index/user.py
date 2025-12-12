"""
前台用户视图模块
实现用户注册、登录、信息管理等功能
"""
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.views import exception_handler

from myapp.auth.authentication import TokenAuthtication
from myapp.auth.throttling import MyRateThrottle
from myapp.handler import APIResponse
from myapp.models import UserInfo, BLogin
from myapp.serializers import UserInfoSerializer, UserInfoDetailSerializer
from myapp.utils import md5value, get_ip, get_ua


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    Args:
        exc: 异常对象
        context: 上下文信息
    Returns:
        APIResponse: 错误响应
    """
    # 调用REST framework默认的异常处理
    response = exception_handler(exc, context)
    if response is not None:
        # 转换为自定义响应格式
        if str(response.data) == "AUTH_FAIL_FRONT":
            return APIResponse(code=403, msg='登录已过期，请重新登录')
        else:
            return APIResponse(code=1, msg='系统错误', data=response.data)
    return response


@api_view(['POST'])
def login(request):
    """
    用户登录接口 - 修复版（明文密码）
    """
    # 同时支持username和user_student_id字段名
    user_student_id = request.data.get('user_student_id', '').strip() or request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()
    
    if not user_student_id or not password:
        return APIResponse(code=1, msg='学号或密码不能为空')
    
    try:
        # 查询用户（使用明文密码）
        user = UserInfo.objects.get(
            user_student_id=user_student_id,
            user_password=password
        )
        
        # 检查用户状态
        if user.user_status == 0:
            return APIResponse(code=1, msg='账号已被禁用')
        
        # 生成Token (使用简单字符串拼接代替MD5)
        token = user_student_id + str(user.user_id)
        
        # 更新用户token
        user.token = token
        user.save()
        
        # 记录登录日志（正确的字段名和值）
        from django.utils import timezone
        BLogin.objects.create(
            user_id=user,
            login_time=timezone.now(),  # 设置当前时间
            ip_address=get_ip(request),
            login_device=get_ua(request),
            login_status=True  # True表示登录成功
        )
        
        # 返回用户信息（不包含密码）
        serializer = UserInfoSerializer(user)
        user_data = serializer.data
        user_data['token'] = token
        
        return APIResponse(code=0, msg='登录成功', data=user_data)
            
    except UserInfo.DoesNotExist:
        # 记录登录失败日志（如果有学号）
        try:
            user = UserInfo.objects.get(user_student_id=user_student_id)
            BLogin.objects.create(
                user_id=user,
                login_time=timezone.now(),
                ip_address=get_ip(request),
                login_device=get_ua(request),
                login_status=False  # False表示登录失败
            )
        except:
            pass
        
        return APIResponse(code=1, msg='学号或密码错误')
    except Exception as e:
        print(f"登录异常: {str(e)}")
        return APIResponse(code=1, msg='系统错误')


@api_view(['POST'])
@throttle_classes([MyRateThrottle])
def register(request):
    """
    用户注册接口（明文密码）
    """
    print(request.data)
    # 同时支持前端发送的字段名和后端期望的字段名
    user_student_id = request.data.get('user_student_id', '').strip() or request.data.get('student_id', '').strip()
    user_name = request.data.get('user_name', '').strip() or request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()
    repassword = request.data.get('repassword', '').strip()
    user_email = request.data.get('user_email', '').strip() or request.data.get('email', '').strip()
    collage = request.data.get('collage', '').strip()
    
    if not user_student_id or not user_name or not password or not repassword or not user_email:
        return APIResponse(code=1, msg='所有字段都不能为空')
    
    if password != repassword:
        return APIResponse(code=1, msg='两次密码不一致')
    
    # 检查学号是否已存在
    users = UserInfo.objects.filter(user_student_id=user_student_id)
    if len(users) > 0:
        return APIResponse(code=1, msg='该学号已注册')
    
    # 检查邮箱是否已存在
    users = UserInfo.objects.filter(user_email=user_email)
    if len(users) > 0:
        return APIResponse(code=1, msg='该邮箱已注册')
    
    # 修复：直接使用UserInfo模型创建，避免序列化器字段映射问题
    try:
        user = UserInfo.objects.create(
            user_student_id=user_student_id,
            user_name=user_name,
            user_email=user_email,
            user_password=password,  # 直接使用明文密码
            user_status=1,
            role='2',
            user_collage=collage  # 保存学院信息（注意拼写：collage）
        )
        
        # 使用序列化器返回数据
        serializer = UserInfoSerializer(user)
        return APIResponse(code=0, msg='注册成功', data=serializer.data)
        
    except Exception as e:
        print(f"注册异常: {str(e)}")
        return APIResponse(code=1, msg='注册失败')  


@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def info(request):
    """
    获取用户信息接口
    Args:
        request: Django请求对象
    Returns:
        APIResponse: 用户信息
    """
    # 支持两种方式获取用户信息：通过token或通过查询参数id
    user_id = request.GET.get('id')
    token = request.META.get("HTTP_TOKEN", "")
    
    try:
        if user_id:
            # 通过用户ID获取信息
            user = UserInfo.objects.get(user_id=user_id)
        else:
            # 通过token获取信息
            users = UserInfo.objects.filter(token=token)
            if len(users) > 0:
                user = users[0]
            else:
                return APIResponse(code=1, msg='用户不存在')
        
        # 使用不包含密码的序列化器
        serializer = UserInfoSerializer(user)
        return APIResponse(code=0, msg='获取成功', data=serializer.data)
    except UserInfo.DoesNotExist:
        return APIResponse(code=1, msg='用户不存在')
    except Exception as e:
        print(f"获取用户信息失败: {str(e)}")
        return APIResponse(code=1, msg='获取失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def update(request):
    """
    更新用户信息接口
    Args:
        request: Django请求对象，包含要更新的用户信息
    Returns:
        APIResponse: 更新结果
    """
    token = request.META.get("HTTP_TOKEN", "")
    users = UserInfo.objects.filter(token=token)
    if len(users) > 0:
        user = users[0]
        # 不允许修改密码和学号
        if 'password' in request.data:
            del request.data['password']
        if 'user_student_id' in request.data:
            del request.data['user_student_id']
        
        # 处理头像上传
        try:
            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                from django.conf import settings
                import os, time
                subdir = 'avatar'
                upload_dir = os.path.join(settings.MEDIA_ROOT, subdir)
                os.makedirs(upload_dir, exist_ok=True)
                ext = os.path.splitext(avatar_file.name)[1] or '.jpg'
                filename = f"{int(time.time()*1000)}{ext}"
                save_path = os.path.join(upload_dir, filename)
                with open(save_path, 'wb') as f:
                    for chunk in avatar_file.chunks():
                        f.write(chunk)
                # 将存储路径写入到请求数据
                request.data['user_avart'] = f"{settings.MEDIA_URL}{subdir}/{filename}"
        except Exception:
            pass

        serializer = UserInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            print(serializer.errors)
            return APIResponse(code=1, msg='更新失败', data=serializer.errors)
    else:
        return APIResponse(code=1, msg='用户不存在')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def updatePwd(request):
    """
    修改密码接口（明文密码）
    Args:
        request: Django请求对象，包含old_password、password、repassword
    Returns:
        APIResponse: 修改结果
    """
    old_password = request.data.get('old_password', None)
    password = request.data.get('password', None)
    repassword = request.data.get('repassword', None)
    
    if not old_password or not password or not repassword:
        return APIResponse(code=1, msg='所有字段都不能为空')
    
    if password != repassword:
        return APIResponse(code=1, msg='两次新密码不一致')
    
    token = request.META.get("HTTP_TOKEN", "")
    users = UserInfo.objects.filter(token=token)
    if len(users) > 0:
        user = users[0]
        
        # 检查旧密码是否正确 - 使用明文密码
        if old_password != user.user_password:
            return APIResponse(code=1, msg='原密码错误')
        
        # 更新密码 - 使用明文密码
        data = {'user_password': password}
        serializer = UserInfoDetailSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='密码修改成功')
        else:
            print(serializer.errors)
    
    return APIResponse(code=1, msg='密码修改失败')
