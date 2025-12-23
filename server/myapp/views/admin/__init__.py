"""
后台管理视图模块
导入所有后台管理相关的视图模块
"""
# 导入各个子模块
from . import overview
from . import product
from . import user
from . import order
from . import comment
from . import category
from . import notice

# 导出所有模块，使其可以通过 views.admin.xxx 访问
__all__ = [
    'overview',
    'product',
    'user',
    'order',
    'comment',
    'category',
    'notice',
]

