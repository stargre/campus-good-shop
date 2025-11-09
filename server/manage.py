#!/usr/bin/env python
"""
Django管理脚本
用于执行Django的各类管理任务，如启动开发服务器、数据库迁移等
"""
import os
import sys


def main():
    """
    Django管理脚本入口函数
    设置Django配置模块并执行命令行管理任务
    """
    # 设置Django配置文件模块路径
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # 执行Django命令行管理任务
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
