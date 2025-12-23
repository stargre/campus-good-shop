"""
URL路由配置模块 - 校园二手交易平台
定义所有API接口的URL路由
"""
from django.urls import path

from myapp import views

app_name = 'myapp'
urlpatterns = [
    # ==================== 后台管理API ====================
    path('admin/overview/count', views.admin.overview.count),
    path('admin/overview/sysInfo', views.admin.overview.sysInfo),
    # 商品管理（替换原thing）
    path('admin/product/list', views.admin.product.list_api),
    path('admin/product/detail', views.admin.product.detail),
    path('admin/product/create', views.admin.product.create),
    path('admin/product/update', views.admin.product.update),
    path('admin/product/delete', views.admin.product.delete),
    # 分类管理
    path('admin/category/list', views.admin.category.list_api),
    path('admin/category/create', views.admin.category.create),
    path('admin/category/update', views.admin.category.update),
    path('admin/category/delete', views.admin.category.delete),
    # 订单管理
    path('admin/order/list', views.admin.order.list_api),
    path('admin/order/detail', views.admin.order.detail),
    path('admin/order/create', views.admin.order.create),
    path('admin/order/update', views.admin.order.update),
    path('admin/order/delete', views.admin.order.delete),
    # 用户管理
    path('admin/user/list', views.admin.user.list_api),
    path('admin/user/create', views.admin.user.create),
    path('admin/user/update', views.admin.user.update),
    path('admin/user/updatePwd', views.admin.user.updatePwd),
    path('admin/user/delete', views.admin.user.delete),
    path('admin/user/info', views.admin.user.info),
    # 管理员登录
    path('admin/adminLogin', views.admin.user.admin_login),
    # 公告管理
    path('admin/notice/list', views.admin.notice.list_api),
    path('admin/notice/create', views.admin.notice.create),
    path('admin/notice/update', views.admin.notice.update),
    path('admin/notice/delete', views.admin.notice.delete),
    # 评论管理
    path('admin/comment/list', views.admin.comment.list_api),
    path('admin/comment/create', views.admin.comment.create),
    path('admin/comment/update', views.admin.comment.update),
    path('admin/comment/delete', views.admin.comment.delete),
    
    # ==================== 前台用户API ====================
    # 用户认证
    path('index/user/login', views.index.user.login),
    path('index/user/register', views.index.user.register),
    path('index/user/info', views.index.user.info),
    path('index/user/update', views.index.user.update),
    path('index/user/updatePwd', views.index.user.updatePwd),
    # 分类管理
    path('index/category/list', views.index.category.list_api),
    path('index/category/detail', views.index.category.detail),
    path('index/category/listWithProducts', views.index.category.listWithProducts),
    # 商品管理
    path('index/product/list', views.index.product.list),
    path('index/product/detail', views.index.product.detail),
    path('index/product/create', views.index.product.create),
    path('index/product/update', views.index.product.update),
    path('index/product/delete', views.index.product.delete),
    path('index/product/myList', views.index.product.myList),
    path('index/product/reserve', views.index.product.reserve),
    path('index/product/cancelReserve', views.index.product.cancel_reserve),
    # 订单管理
    path('index/order/list', views.index.order.list_api),
    path('index/order/detail', views.index.order.detail_api),
    path('index/order/create', views.index.order.create),
    path('index/order/cancel', views.index.order.cancel_order),
    path('index/order/pay', views.index.order.pay),
    path('index/order/confirm', views.index.order.confirm_receipt),
    path('index/order/evaluate', views.index.order.evaluate),
    path('index/order/deliver', views.index.order.deliver),
    path('index/order/refund', views.index.order.refund),
    path('index/order/buyer-cancel-paid', views.index.order.buyer_cancel_paid_order),
    # 系统通知
    path('index/notice/list', views.index.notice.list_api),
    # 搜索功能
    path('index/search/search', views.index.search),
    path('index/search/hotKeywords', views.index.hotKeywords),
    # 地址管理
    path('index/address/list', views.index.address.list_api),
    path('index/address/create', views.index.address.create),
    path('index/address/update', views.index.address.update),
    path('index/address/delete', views.index.address.delete),
    # 收藏功能
    path('index/favorite/add', views.index.favorite.add),
    path('index/favorite/remove', views.index.favorite.remove),
    path('index/favorite/batchRemove', views.index.favorite.batchRemove),
    path('index/favorite/list', views.index.favorite.list),
    # 评论功能
    path('index/comment/list', views.index.comment.list_api),
    path('index/comment/listMyComments', views.index.comment.list_my_comment),
    path('index/comment/create', views.index.comment.create),
    path('index/comment/like', views.index.comment.like),
    path('index/comment/delete', views.index.comment.delete),

]
