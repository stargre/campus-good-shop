from myapp.views.index.category import *
from myapp.views.index.user import *
from myapp.views.index.comment import *
from myapp.views.index.order import *
from myapp.views.index.notice import *
from myapp.views.index.address import *
from myapp.views.index.product import *
from myapp.views.index.search import *
from myapp.views.index.record import *
from myapp.views.index.cart import *
from myapp.views.index.favorite import *

# 暴露子模块以支持 views.index.xxx 访问
from . import category as category
from . import user as user
from . import comment as comment
from . import order as order
from . import notice as notice
from . import address as address
from . import product as product
from . import search as search
from . import record as record
from . import cart as cart
from . import favorite as favorite
try:
    from . import upload as upload
except Exception:
    pass

__all__ = [
    'category', 'user', 'comment', 'order', 'notice', 'address', 'product', 'search', 'record', 'cart', 'favorite', 'upload'
]
