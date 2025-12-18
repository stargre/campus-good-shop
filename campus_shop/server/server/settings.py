"""
Django项目配置文件
包含数据库、中间件、应用、跨域等配置

注意：生产环境需要修改以下配置：
1. SECRET_KEY - 改为随机生成的密钥
2. DEBUG - 改为 False
3. ALLOWED_HOSTS - 限制允许的主机
4. 数据库密码 - 使用环境变量或配置文件管理
"""
import os
from pathlib import Path

# 项目根目录路径
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==================== 安全配置 ====================
# SECURITY WARNING: 生产环境必须修改密钥！
SECRET_KEY = 'django-insecure-sz@madp0ifx!b)^lg_g!f+5s*w7w_=sjgq-k+erzb%x42$^r!d'

# SECURITY WARNING: 生产环境必须关闭调试模式！
DEBUG = True

# 允许的主机（生产环境应限制为具体域名）
ALLOWED_HOSTS = ['*']

# ==================== 应用配置 ====================
INSTALLED_APPS = [
    'django.contrib.admin',  # Django管理后台
    'django.contrib.auth',  # 认证系统
    'django.contrib.contenttypes',  # 内容类型框架
    'django.contrib.sessions',  # 会话框架
    'django.contrib.messages',  # 消息框架
    'django.contrib.staticfiles',  # 静态文件处理
    'rest_framework',  # Django REST Framework
    'corsheaders',  # 跨域处理
    'myapp'  # 主应用
]

# ==================== 中间件配置 ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话中间件
    'corsheaders.middleware.CorsMiddleware',  # 跨域中间件（必须在CommonMiddleware之前）
    'django.middleware.common.CommonMiddleware',  # 通用中间件
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF保护中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持保护
    'myapp.middlewares.LogMiddleware.OpLogs'  # 自定义操作日志中间件
]

# ==================== 跨域配置 ====================
# 注意：生产环境应限制允许的源
CORS_ORIGIN_ALLOW_ALL = True  # 允许所有源跨域（开发环境）

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

# ==================== 数据库配置 ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # MySQL数据库引擎
        'NAME': 'campus_shop',  # 数据库名
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'lzylzy123',  # 数据库密码（在这里替换成你自己的）
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': '3306',  # 数据库端口
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",  # 禁用外键检查
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/


LANGUAGE_CODE = 'zh-hans'

# 时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# 日期时间格式
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'

# ==================== 文件上传配置 ====================
# 媒体文件存储路径（用户上传的文件）
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/')
MEDIA_URL = '/upload/'  # 媒体文件URL前缀

# ==================== 静态文件配置 ====================
# 静态文件URL前缀（CSS、JavaScript、Images等）
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== 跨域详细配置 ====================
CORS_ALLOW_CREDENTIALS = True  # 允许携带凭证
CORS_ALLOW_ALL_ORIGINS = True  # 允许所有源（生产环境应限制）
CORS_ALLOW_HEADERS = '*'  # 允许所有请求头

# 在 settings.py 中添加或修改
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # 启用API浏览器
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# 开发时将邮件输出到控制台，便于调试找回密码流程；上线请替换为真实 SMTP 配置
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Example SMTP settings (uncomment and configure for production)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'your@example.com'
# EMAIL_HOST_PASSWORD = 'password'
# EMAIL_USE_TLS = True