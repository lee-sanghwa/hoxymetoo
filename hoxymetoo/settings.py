"""
프로그램 ID:SV-1900-PY
프로그램명:settings.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- Django 서버의 전반적인 환경설정파일이다.
"""

import os
from logging import Handler
from datetime import datetime
from hoxymetoo.key import mysql_conf


class HttpHandler(Handler):
    def emit(self, record):
        request = record.args[0]
        record.ip = request.META.get('HTTP_X_FORWARDED_FOR')
        record.args = None

        return super(HttpHandler, self).emit(record)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vtas7d1^%7diibfpxg=gd)3_er-n9k@csfdwn5l4w=wx_o^nkj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# debug_toolbar의 사용을 위한 설정 (로컬 호스트에서만)
INTERNAL_IPS = ('127.0.0.1')

# Django 서버에 어떤 아이피가 접속가능하게 할 것인가? (모두 다)
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'addresses',
    'members',
    'welfares',
    'qnas',
    'chatbot',
    'receivableMoney',
    'debug_toolbar'
]

# django rest framework의 설정
REST_FRAMEWORK = {
    # 한 페이지에 최대 10개의 정보를 제공
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'hoxymetoo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'hoxymetoo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # ./key.py 에 db정보를 담아두고 있다.
    'default': mysql_conf
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'hoxymetoo', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

today_date = datetime.now().strftime("%Y-%m-%d")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'common_format': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(ip)s  %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'common_format',
            'filename': f'{os.fspath(BASE_DIR)}/{today_date}_debug.log'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'addresses': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'chatbot': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'members': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'receivableMoney': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'welfares': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
