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
    # 系统日志
    path('admin/errorLog/list', views.admin.errorLog.list_api),
    path('admin/loginLog/list', views.admin.loginLog.list_api),
    path('admin/opLog/list', views.admin.opLog.list_api),
    # 公告管理
    path('admin/notice/list', views.admin.notice.list_api),
    path('admin/notice/create', views.admin.notice.create),
    path('admin/notice/update', views.admin.notice.update),
    path('admin/notice/delete', views.admin.notice.delete),


    # ==================== 前台用户API ====================
    # 用户认证
    path('index/user/login', views.index.user.login),
    path('index/user/register', views.index.user.register),
    path('index/user/info', views.index.user.info),
    path('index/user/update', views.index.user.update),
    path('index/user/updatePwd', views.index.user.updatePwd),
    # 分类管理
    path('index/category/list_api', views.index.category.list_api),
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
    # 订单管理
    path('index/order/list', views.index.order.list_api),
    path('index/order/detail', views.index.order.detail_api),
    path('index/order/create', views.index.order.create),
    path('index/order/cancel', views.index.order.cancel_order),
    path('index/order/pay', views.index.order.pay),
    path('index/order/confirm', views.index.order.confirm_receipt),
    path('index/order/evaluate', views.index.order.evaluate),
    # 预约管理
    path('index/reserve/create', views.index.order.reserve_create),
    path('index/reserve/list', views.index.order.reserve_list),
    path('index/reserve/cancel', views.index.order.cancel_reserve),
    # 系统通知
    path('index/notice/list', views.index.notice.list_api),
    # 标签管理
    path('index/tag/list_api', views.index.tag.list_api),
    path('index/tag/detail', views.index.tag.detail),
    path('index/tag/listWithProducts', views.index.tag.listWithProducts),
    # 搜索功能
    path('index/search/search', views.index.search.search),
    path('index/search/hotKeywords', views.index.search.hotKeywords),
    # 浏览记录
    path('index/record/list', views.index.record.list_api),
    path('index/record/create', views.index.record.create),
    path('index/record/delete', views.index.record.delete),
    path('index/record/deleteAll', views.index.record.deleteAll),
    # 购物车
    path('index/cart/list', views.index.cart.list_api),
    path('index/cart/add', views.index.cart.add),
    path('index/cart/delete', views.index.cart.delete),
    path('index/cart/deleteAll', views.index.cart.deleteAll),
    # 地址管理
    path('index/address/list', views.index.address.list_api),
    path('index/address/create', views.index.address.create),
    path('index/address/update', views.index.address.update),
    path('index/address/delete', views.index.address.delete),


]
