# apply_migrations.py （其实这名字不合适，建议叫 init_data.py 或类似）

import os
import django
from django.conf import settings

# 设置 Django 配置模块（根据你的项目结构调整）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# 启动 Django
django.setup()

# 现在可以安全导入模型
from myapp.models import UserInfo

# 示例：更新 admin 用户的 role
user = UserInfo.objects.filter(user_name='admin').first()
if user:
    user.role = '1'
    user.save()
    print("✅ 更新成功：admin 的 role 已设为 '1'")
else:
    print("❌ 未找到 user_student_id 为 'admin' 的用户")