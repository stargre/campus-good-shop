"""
Django项目主URL配置
定义项目的URL路由规则
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from server import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理后台
    path('myapp/', include('myapp.urls')),  # 主应用路由
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 媒体文件服务
