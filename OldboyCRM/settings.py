#_*_encoding:utf-8_*_
"""
Django settings for OldboyCRM project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!_ozu*fpy09_)o)kutimblfxqn6j9(q#57s6_q*dws!ef-lh*f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.humanize',
    'crm',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'OldboyCRM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS':True,
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

WSGI_APPLICATION = 'OldboyCRM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ooold',
        'HOST':'',
        'PORT':'',
        'USER':'root',
        'PASSWORD':'123456',
    }
}



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    "%s/%s" %(BASE_DIR, "statics"),
)



AUTH_USER_MODEL = 'crm.UserProfile'

LOGIN_URL = '/crm/login/'

ENROLL_DATA_DIR = "%s/enrolled_data"  % BASE_DIR
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60*60*2

############################################
# 初始化系统默认logs 只当系统是linux的时候.才进行相关的日志初始化工作
#LOGGING_stamdard_format = '[%(asctime)s][task_id:%(name)s][%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s'
#LOGGING_simple_format = '[%(filename)s:%(lineno)d][%(levelname)s] %(message)s'
#LOGGING_request_format = '[%(asctime)s][%(status_code)s][%(request)s] %(message)s'
#REST_SESSION_LOGIN = False
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,  # this fixes the problem
#    'formatters': {
#        'standard': {  # 详细
#            'format': LOGGING_stamdard_format
#        },
#        'simple': {  # 简单
#            'format': LOGGING_simple_format
#        },
#        'request': {  # 简单
#            'format': LOGGING_request_format
#        },
#    },
#    'filters': {},
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler',
#            'include_html': True,
#        },
#        'console':{
#            'level': 'INFO',
#            'class': 'logging.StreamHandler',  # 打印到前台
#            'formatter': 'simple'
#        },
#        'default': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': os.path.join(BASE_DIR+'/logs/','all.log'),
#
#            'maxBytes': 1024*1024*10,
#            'backupCount': 5,
#            'formatter':'standard',
#       'request': {
#
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': os.path.join(BASE_DIR+'/logs/','request.log'),
#
#            'maxBytes': 1024*1024*10,
#            'backupCount': 5,
#            'formatter':'request',
#        },
#        'db': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#
#
#            'maxBytes': 1024*1024*10,
#            'backupCount': 5,
#            'formatter':'standard',
#        },
#
#    'loggers': {
#        'django': {
#            'handlers': ['default','console'],
#            'propagate': False,
#            'level': 'DEBUG',
#        },
#        'django.request': {
#            'handlers': ['request','default'],
#            'level': 'DEBUG',
#            'propagate': False,
#        },
#        'django.db.backends':{
#            'handlers': ['db'],
#            'level': 'DEBUG',
#            'propagate': False
#        },
#    }
#}

#'''
#try:
#    from .settings_dev import *
#except Exception as e:
#    print(u'无法找到settings_dev文件.开启生产模式')
#    print(e.message)
#'''