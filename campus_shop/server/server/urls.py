"""
Django项目主URL配置
定义项目的URL路由规则
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from server import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理后台
    path('myapp/', include('myapp.urls')),  # 主应用路由
    # 显式媒体文件服务（即使 DEBUG=False 也可在本地开发访问）
    re_path(r'^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 媒体文件服务
