"""
后台用户管理视图模块 - 修复版
"""
from rest_framework.decorators import api_view, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import UserInfo
from myapp.serializers import UserInfoSerializer, UserInfoDetailSerializer


@api_view(['POST'])
@csrf_exempt
def admin_login(request):
    """
    管理员登录接口 - 简化版
    """
    try:
        print("\n=== 管理员登录请求开始 ===")
        
        # 获取请求数据
        student_id = ''
        password = ''
        
        try:
            # 尝试获取请求数据
            if request.method == 'POST':
                if hasattr(request, 'data') and request.data:
                    student_id = request.data.get('username', '').strip()
                    password = request.data.get('password', '').strip()
                else:
                    # 尝试解析JSON
                    import json
                    data = json.loads(request.body.decode('utf-8'))
                    student_id = data.get('username', '').strip()
                    password = data.get('password', '').strip()
        except Exception as e:
            print(f"获取请求数据失败: {str(e)}")
            return APIResponse(code=1, msg='请求数据格式错误')
        
        print(f"用户名: '{student_id}', 密码: '{password}'")
        
        # 验证输入
        if not student_id or not password:
            return APIResponse(code=1, msg='学号和密码不能为空')
        
        # 查询用户
        try:
            user = UserInfo.objects.get(user_student_id=student_id)
            print(f"找到用户: {user.user_name}, 角色: {user.role}")
            
            # 验证密码
            if user.user_password != password:
                return APIResponse(code=1, msg='学号或密码错误')
            
            # 验证角色
            if user.role not in ['0', '1', '3','A']:
                return APIResponse(code=1, msg='该账号不是管理员账号')
            
            # 验证状态
            if user.user_status == 0:
                return APIResponse(code=1, msg='账号已被禁用')
            
            # 生成并更新token
            token = student_id + 'admin'
            user.token = token
            user.save()
            # 将管理员 id 写入 session，以便后续不依赖 token 进行认证
            try:
                request.session['admin_user_id'] = user.user_id
                request.session.modified = True
                print(f'已写入 session admin_user_id={user.user_id}')
            except Exception as e:
                print(f'写入 session 失败: {e}')
            
            # 构建响应数据
            response_data = {
                'id': user.user_id,
                'username': user.user_student_id,
                'nickname': user.user_name,
                'token': token
            }
            
            print("登录成功")
            return APIResponse(code=0, msg='登录成功', data=response_data)
            
        except UserInfo.DoesNotExist:
            print("用户不存在")
            return APIResponse(code=1, msg='学号或密码错误')
            
    except Exception as e:
        print(f"登录接口异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return APIResponse(code=1, msg='登录失败，请稍后重试')
    finally:
        print("=== 管理员登录请求结束 ===\n")


@api_view(['GET'])
@csrf_exempt
@authentication_classes([AdminTokenAuthtication])
def list_api(request):
    """
    用户列表接口
    """
    try:
        # 获取查询参数
        keyword = request.GET.get('keyword', '')
        role = request.GET.get('role', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # 构建查询条件
        queryset = UserInfo.objects.all()
        
        # 关键词搜索
        if keyword:
            queryset = queryset.filter(
                Q(user_student_id__contains=keyword) |
                Q(user_name__contains=keyword) |
                Q(user_email__contains=keyword)
            )
        
        # 角色筛选
        if role:
            queryset = queryset.filter(role=role)
        
        # 总数
        total = queryset.count()
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        users = queryset.order_by('-user_create_time')[start:end]
        
        # 序列化
        serializer = UserInfoSerializer(users, many=True)
        
        # 前端期望直接返回数组
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
        
    except Exception as e:
        print(f"用户列表查询失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['GET'])
@csrf_exempt
@authentication_classes([AdminTokenAuthtication])
def info(request):
    """
    用户详情接口 - 实现版
    """
    try:
        user_id = request.GET.get('id')
        if not user_id:
            return APIResponse(code=1, msg='用户ID不能为空')
        
        user = UserInfo.objects.get(user_id=user_id)
        serializer = UserInfoDetailSerializer(user)
        
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
        
    except UserInfo.DoesNotExist:
        return APIResponse(code=1, msg='用户不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'查询失败: {str(e)}')


@api_view(['POST'])
@csrf_exempt
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """
    创建用户接口 - 修复版（支持前端字段映射）
    """
    try:
        data = request.data.copy()
        print(f"创建用户请求数据: {data}")
        
        # 处理前端字段到后端模型字段的映射
        # 前端使用username，后端使用user_student_id
        if 'username' in data and not data.get('user_student_id'):
            data['user_student_id'] = data['username']
        
        # 前端使用nickname，后端使用user_name
        if 'nickname' in data and not data.get('user_name'):
            data['user_name'] = data['nickname']
        
        # 前端使用status，后端使用user_status
        if 'status' in data and not data.get('user_status'):
            data['user_status'] = data['status']
        
        # 前端使用email，后端使用user_email
        if 'email' in data and not data.get('user_email'):
            data['user_email'] = data['email']
        
        # 必填字段验证
        required_fields = ['user_student_id', 'user_name', 'user_email']
        for field in required_fields:
            if not data.get(field):
                return APIResponse(code=1, msg=f'{field}不能为空')
        
        # 检查学号是否重复
        if UserInfo.objects.filter(user_student_id=data['user_student_id']).exists():
            return APIResponse(code=1, msg='学号已存在')
        
        # 检查邮箱是否重复
        if UserInfo.objects.filter(user_email=data['user_email']).exists():
            return APIResponse(code=1, msg='邮箱已存在')
        
        # 设置默认密码（学号后6位）- 明文存储
        if 'password' in data and data['password']:
            data['user_password'] = data['password']
        elif 'user_password' not in data or not data['user_password']:
            data['user_password'] = data['user_student_id'][-6:]
        
        # 设置默认角色为普通用户
        if 'role' not in data:
            data['role'] = '2'
        
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        else:
            print(f"序列化器错误: {serializer.errors}")
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
            
    except Exception as e:
        print(f"创建用户失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return APIResponse(code=1, msg=f'创建失败: {str(e)}')


@api_view(['POST'])
@csrf_exempt
@authentication_classes([AdminTokenAuthtication])
def update(request):
    """
    更新用户接口 - 实现版
    """
    try:
        user_id = request.data.get('user_id') or request.GET.get('id') or request.data.get('id')
        if not user_id:
            return APIResponse(code=1, msg='用户ID不能为空')
        
        user = UserInfo.objects.get(user_id=user_id)
        data = request.data.copy()
        
        # 移除不能修改的字段
        data.pop('user_password', None)
        data.pop('user_student_id', None)  # 学号不可修改
        
        # 检查邮箱是否重复（排除自己）
        if 'user_email' in data and data['user_email'] != user.user_email:
            if UserInfo.objects.filter(user_email=data['user_email']).exclude(user_id=user_id).exists():
                return APIResponse(code=1, msg='邮箱已存在')
        
        serializer = UserInfoSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='参数错误', data=serializer.errors)
            
    except UserInfo.DoesNotExist:
        return APIResponse(code=1, msg='用户不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'更新失败: {str(e)}')


@api_view(['POST'])
@csrf_exempt
@authentication_classes([AdminTokenAuthtication])
def updatePwd(request):
    """
    修改密码接口 - 实现版（明文密码）
    """
    try:
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')
        
        if not user_id or not new_password:
            return APIResponse(code=1, msg='用户ID和新密码不能为空')
        
        user = UserInfo.objects.get(user_id=user_id)
        
        # 更新密码（明文存储）
        user.user_password = new_password
        user.save()
        
        return APIResponse(code=0, msg='密码修改成功')
        
    except UserInfo.DoesNotExist:
        return APIResponse(code=1, msg='用户不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'密码修改失败: {str(e)}')


@api_view(['POST'])
@csrf_exempt
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    """
    删除用户接口 - 实现版
    """
    try:
        user_id = request.data.get('user_id') or request.GET.get('id') or request.data.get('id') or request.GET.get('ids')
        if not user_id:
            return APIResponse(code=1, msg='用户ID不能为空')
        
        # 不能删除自己
        current_user = request.user
        if current_user.user_id == int(user_id):
            return APIResponse(code=1, msg='不能删除自己的账号')
        
        user = UserInfo.objects.get(user_id=user_id)
        user.delete()
        
        return APIResponse(code=0, msg='删除成功')
        
    except UserInfo.DoesNotExist:
        return APIResponse(code=1, msg='用户不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'删除失败: {str(e)}')


 
