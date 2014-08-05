# -*- encoding: utf8 -*-
"""
Django settings for tshapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secretkey'

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['tsh.adiq.eu']


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'multitest',
    'multitest_admin',
    'inplaceeditform',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tshapp.urls'
WSGI_APPLICATION = 'tshapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbname',
        'USER': 'user',
        'PASSWORD': 'secret',
        'HOST': 'localhost',
        'PORT': ''
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = PROJECT_PATH + '/tshapp/media/'
MEDIA_URL = '/media/'


STATIC_ROOT = PROJECT_PATH + '/tshapp/static/'
STATIC_URL = '/static/'


# Template files location

TEMPLATE_DIRS = (
    PROJECT_PATH + "/tshapp/templates"
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

# Mailing config
# Setup SMTP for sending emails

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'poczta.o2.pl'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sample@o2.pl'
EMAIL_HOST_PASSWORD = 'secret password'


# Development settings
# SECURITY WARNING: never use settings below on production!

# DEBUG = True
# TEMPLATE_DEBUG = True
# ALLOWED_HOSTS = []
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
# }
#
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'