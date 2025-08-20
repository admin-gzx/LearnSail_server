"""
Django设置文件 for learn_sail项目.

由'django-admin startproject'使用Django 4.2.11生成.

有关此文件的更多信息，请参阅
https://docs.djangoproject.com/en/4.2/topics/settings/

有关设置及其值的完整列表，请参阅
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# 构建项目内路径，例如: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# 快速启动开发设置 - 不适合生产环境
# 请参阅 https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# 安全警告: 在生产环境中请保持密钥的机密性!
SECRET_KEY = 'django-insecure-ks(tuk8%b7nxz5)*$(6-om(pzm-w6$l#l67l^np%)@a#fi%qh6'

# 安全警告: 在生产环境中不要开启DEBUG模式!
DEBUG = True

# 允许访问的主机列表
ALLOWED_HOSTS = []


# 应用定义
INSTALLED_APPS = [
    'django.contrib.admin',          # Django管理后台
    'django.contrib.auth',           # 认证系统
    'django.contrib.contenttypes',   # 内容类型框架
    'django.contrib.sessions',       # 会话管理
    'django.contrib.messages',       # 消息框架
    'django.contrib.staticfiles',    # 静态文件管理
    'rest_framework',                # Django REST Framework
    'corsheaders',                   # CORS跨域请求处理
    'users',                         # 用户应用
    'courses',                       # 课程应用
    'learning',                      # 学习记录应用
    'homework',                      # 作业应用
    'exams',                         # 考试应用
    'community',                     # 社区应用
    'analytics',                     # 数据分析应用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话中间件
    'corsheaders.middleware.CorsMiddleware',  # CORS中间件
    'django.middleware.common.CommonMiddleware',  # 通用中间件
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF保护中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持保护中间件
]

ROOT_URLCONF = 'learn_sail.urls'  # 根URL配置模块

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 模板后端
        'DIRS': [],  # 模板目录列表
        'APP_DIRS': True,  # 是否在应用目录中查找模板
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # 调试上下文处理器
                'django.template.context_processors.request',  # 请求上下文处理器
                'django.contrib.auth.context_processors.auth',  # 认证上下文处理器
                'django.contrib.messages.context_processors.messages',  # 消息上下文处理器
            ],
        },
    },
]

WSGI_APPLICATION = 'learn_sail.wsgi.application'  # WSGI应用入口


# 数据库配置
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'learn_sail_db',  # 数据库名称
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库密码
        'HOST': 'localhost',  # 数据库主机
        'PORT': '3306',  # 数据库端口
        'OPTIONS': {
            'charset': 'utf8mb4',  # 数据库字符集
        },
    }
}


# 密码验证配置
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # 用户名相似性验证
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # 最小长度验证
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # 常见密码验证
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # 数字密码验证
    },
]


# 国际化设置
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'  # 语言代码

TIME_ZONE = 'UTC'  # 时区

USE_I18N = True  # 是否启用国际化

USE_TZ = True  # 是否使用时区支持


# 静态文件设置 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'  # 静态文件URL前缀

# 默认主键字段类型
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # 默认自动字段类型

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'  # 指定自定义用户模型

# REST Framework设置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 默认权限类：需要认证
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # 会话认证
        'rest_framework.authentication.BasicAuthentication',  # 基本认证
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT认证
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # 默认分页类
    'PAGE_SIZE': 10  # 每页记录数
}

# JWT设置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),  # 访问令牌有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # 刷新令牌有效期
    'ROTATE_REFRESH_TOKENS': False,  # 是否旋转刷新令牌
    'BLACKLIST_AFTER_ROTATION': False,  # 是否在旋转后加入黑名单
    'UPDATE_LAST_LOGIN': True,  # 是否更新最后登录时间

    'ALGORITHM': 'HS256',  # 加密算法
    'SIGNING_KEY': SECRET_KEY,  # 签名密钥
    'VERIFYING_KEY': None,  # 验证密钥
    'AUDIENCE': None,  # 受众
    'ISSUER': None,  # 签发者

    'AUTH_HEADER_TYPES': ('Bearer',),  # 认证头类型
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # 认证头名称
    'USER_ID_FIELD': 'id',  # 用户ID字段
    'USER_ID_CLAIM': 'user_id',  # 用户ID声明

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # 认证令牌类
    'TOKEN_TYPE_CLAIM': 'token_type',  # 令牌类型声明

    'JTI_CLAIM': 'jti',  # JWT ID声明

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',  # 滑动令牌刷新过期声明
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),  # 滑动令牌有效期
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # 滑动令牌刷新有效期
}

# CORS设置
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',  # 允许的源
    'http://127.0.0.1:8080',
]

# Redis缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',  # 缓存后端
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis连接地址
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',  # 客户端类
        }
    }
}

# 媒体文件设置
MEDIA_URL = '/media/'  # 媒体文件URL前缀
MEDIA_ROOT = BASE_DIR / 'media'  # 媒体文件存储根目录

# 日志设置
LOGGING = {
    'version': 1,  # 日志版本
    'disable_existing_loggers': False,  # 是否禁用现有日志器
    'handlers': {
        'file': {
            'level': 'INFO',  # 日志级别
            'class': 'logging.FileHandler',  # 文件处理器
            'filename': BASE_DIR / 'logs/learn_sail.log',  # 日志文件路径
        },
        'console': {
            'level': 'INFO',  # 日志级别
            'class': 'logging.StreamHandler',  # 控制台处理器
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],  # 使用的处理器
            'level': 'INFO',  # 日志级别
            'propagate': True,  # 是否传播日志
        },
    },
}
