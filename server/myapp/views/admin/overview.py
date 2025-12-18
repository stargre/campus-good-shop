"""
后台总览视图模块
提供数据统计和系统信息接口
"""
from datetime import datetime, timedelta
from django.db import models
from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import UserInfo, Product, UserOrder, BNotice, BLogin


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def count(request):
    """
    获取数据统计接口
    返回：前端统计分析页面期望的数据格式
    """
    try:
        # 获取今日日期范围
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # 获取近7天日期范围
        week_ago = today_start - timedelta(days=7)
        
        # 商品统计
        product_count = Product.objects.count()
        # 本周新增商品数（从7天前到现在）
        product_week_count = Product.objects.filter(
            create_time__gte=week_ago
        ).count()
        
        # 订单统计 - 按状态分类
        # 未付订单（假设订单状态0表示未支付）
        order_not_pay_count = UserOrder.objects.filter(order_status=0).count()
        # 未付订单的用户数
        order_not_pay_p_count = UserOrder.objects.filter(order_status=0).values('user_id').distinct().count()
        
        # 已付订单（假设订单状态1、2、3表示已支付或已完成）
        order_payed_count = UserOrder.objects.filter(order_status__in=[1, 2, 3]).count()
        # 已付订单的用户数
        order_payed_p_count = UserOrder.objects.filter(order_status__in=[1, 2, 3]).values('user_id').distinct().count()
        
        # 取消订单（假设订单状态4表示已取消）
        order_cancel_count = UserOrder.objects.filter(order_status=4).count()
        # 取消订单的用户数
        order_cancel_p_count = UserOrder.objects.filter(order_status=4).values('user_id').distinct().count()
        
        # 最近一周访问量数据（模拟数据，实际应该从访问日志表获取）
        visit_data = []
        for i in range(7):
            day = (week_ago + timedelta(days=i)).strftime('%m-%d')
            visit_data.append({
                'day': day,
                'uv': 100 + i * 10,  # 模拟UV数据
                'pv': 200 + i * 20   # 模拟PV数据
            })
        
        # 额外统计：用户、分类、评论、订单总数
        try:
            from myapp.models import Comment, Category
            comment_count = Comment.objects.count()
        except Exception:
            comment_count = 0
        try:
            from myapp.models import Category
            category_count = Category.objects.count()
        except Exception:
            category_count = 0
        user_count = UserInfo.objects.count()
        order_count = UserOrder.objects.count()

        # 构建返回数据 - 包含新的统计项，移除或保留 visit_data 由前端决定
        data = {
            'product_count': product_count,
            'product_week_count': product_week_count,
            'order_not_pay_count': order_not_pay_count,
            'order_not_pay_p_count': order_not_pay_p_count,
            'order_payed_count': order_payed_count,
            'order_payed_p_count': order_payed_p_count,
            'order_cancel_count': order_cancel_count,
            'order_cancel_p_count': order_cancel_p_count,
            'visit_data': visit_data,
            'comment_count': comment_count,
            'user_count': user_count,
            'category_count': category_count,
            'order_count': order_count
        }
        
        return APIResponse(code=0, msg='获取成功', data=data)
        
    except Exception as e:
        return APIResponse(code=1, msg=f'获取失败: {str(e)}')


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def sysInfo(request):
    """
    获取系统信息接口 - 简化版（不依赖psutil）
    """
    try:
        import platform
        import django
        from django.db import connection
        import os
        import socket
        import sys
        
        # 获取系统信息
        system_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'hostname': socket.gethostname(),
            'ip_address': socket.gethostbyname(socket.gethostname()),
            'python_executable': sys.executable,
        }
        
        # 获取Django信息
        django_info = {
            'version': django.get_version(),
            'debug_mode': os.environ.get('DJANGO_DEBUG', 'False') == 'True',
            'timezone': django.conf.settings.TIME_ZONE,
            'language_code': django.conf.settings.LANGUAGE_CODE,
            'installed_apps_count': len(django.conf.settings.INSTALLED_APPS),
        }
        
        # 获取数据库信息
        db_info = {
            'engine': connection.vendor,
            'database_name': connection.settings_dict['NAME'],
            'tables_count': len(connection.introspection.table_names()),
        }
        
        # 获取项目信息
        project_info = {
            'base_dir': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'server_start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 简化，实际应该记录启动时间
        }
        
        # 构建返回数据，兼容前端sys-info.vue期望的字段
        try:
            import locale
            import time
            # 尝试使用psutil获取更详细的资源信息
            try:
                import psutil
                vm = psutil.virtual_memory()
                total_gb = round(vm.total / (1024 ** 3), 2)
                used_gb = round((vm.total - vm.available) / (1024 ** 3), 2)
                percent_memory = round(vm.percent, 1)
                cpu_load = round(psutil.cpu_percent(interval=0.1), 1)
            except Exception:
                total_gb = None
                used_gb = None
                percent_memory = None
                cpu_load = None

            ret = {
                'sysName': platform.system() + ' ' + platform.release(),
                'versionName': platform.version(),
                'osName': system_info.get('platform'),
                'pf': platform.machine(),
                'cpuCount': os.cpu_count(),
                'processor': platform.processor(),
                'cpuLoad': cpu_load if cpu_load is not None else 0,
                'memory': total_gb if total_gb is not None else 0,
                'usedMemory': used_gb if used_gb is not None else 0,
                'percentMemory': percent_memory if percent_memory is not None else 0,
                'sysLan': locale.getdefaultlocale()[0] if locale.getdefaultlocale() else '',
                'sysZone': time.tzname[0] if hasattr(time, 'tzname') else '',
                'mysqlVersion': '5.7.37',
                'nginxVersion': '1.20.1'
            }

            # 项目与数据库信息也加入data中，供管理员查看
            ret['projectBaseDir'] = project_info.get('base_dir')
            ret['databaseName'] = db_info.get('database_name')
            ret['tablesCount'] = db_info.get('tables_count')

            return APIResponse(code=0, msg='获取成功', data=ret)
        except Exception as e:
            return APIResponse(code=0, msg='获取成功', data={
                'sysName': system_info,
                'django': django_info,
                'database': db_info,
                'project': project_info
            })
        
    except Exception as e:
        return APIResponse(code=1, msg=f'获取失败: {str(e)}')