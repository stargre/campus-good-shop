"""
后台管理视图模块入口
导入admin目录下的子模块，使其可以通过 views.admin.xxx 访问

注意：此文件用于兼容 urls.py 中的 views.admin.xxx 调用方式
实际的后台视图模块在 admin/ 目录下
"""
# 从admin子目录导入各个模块（admin是目录，不是文件）
# 由于admin是目录，需要通过admin目录下的__init__.py导入
from myapp.views.admin import overview
from server.myapp.views.admin import product
from myapp.views.admin import user
from myapp.views.admin import order
from myapp.views.admin import comment
from myapp.views.admin import classification
from server.myapp.views.admin import category
from myapp.views.admin import notice
from myapp.views.admin import ad
from myapp.views.admin import banner
from myapp.views.admin import record
from myapp.views.admin import loginLog
from myapp.views.admin import opLog
from myapp.views.admin import errorLog

# 导出admin模块，使其可以通过 views.admin.xxx 访问
__all__ = [
    'overview',
    'product',
    'user',
    'order',
    'comment',
    'classification',
    'category',
    'notice',
    'ad',
    'banner',
    'record',
    'loginLog',
    'opLog',
    'errorLog',
]