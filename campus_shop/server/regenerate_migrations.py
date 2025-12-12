#!/usr/bin/env python
"""
生成新迁移以添加cover_image_id
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from django.core.management import call_command

# 尝试生成新迁移
print("正在生成新迁移...")
try:
    call_command('makemigrations', 'myapp', verbosity=2)
except Exception as e:
    print(f"生成迁移出错: {e}")

# 然后应用迁移
print("\n正在应用迁移...")
try:
    call_command('migrate', 'myapp', verbosity=2)
except Exception as e:
    print(f"应用迁移出错: {e}")
