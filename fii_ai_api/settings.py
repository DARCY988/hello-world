"""
Django settings for Fii AI API project.

Generated by 'django-admin startproject' using Django 2.1.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import socket
import importlib
from corsheaders.defaults import default_headers


# System will add contributors from each App in this api project
# Need to modified this on your own project/config.py
__CONTRIBUTORS__ = ['Bean Yen', 'Travis Lu', 'Jean Yuan', 'Ivy Kao']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8_8q^6$bc2=mwhkud99v@j^7zmf86wcjgfha_w@ovn-+4a5eke'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    # default dependencies
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # import new dependencies
    'django_crontab',
    'rest_framework',
    'django_filters',
    'corsheaders',
    # project list
    'demo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fii_ai_api.urls'

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
            ]
        },
    }
]

WSGI_APPLICATION = 'fii_ai_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, 'db.sqlite3')},
    'fii-ai': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '10.124.131.87',
        'PORT': 3306,
        'USER': 'api',
        'PASSWORD': 'Develop123!@#',
        'NAME': 'init',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/opt/media/'


# API version control
__API_VERSION__ = set(['fii-api/latest'])

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Allowed Headers List
CORS_ALLOW_HEADERS = list(default_headers) + ['user-id']

# Inital Jobs List
CRONJOBS = [
    # this is just a demo job.
    # ('*/5 * * * *', 'demo.cron.my_cron_job_demo', '>> /srv/logs/demo_cron_job.log'),
]

# Load CORS Jobs
for app in INSTALLED_APPS:
    # if 'demo' in app:
    #     continue
    if 'django' in app:
        continue
    if app in ['rest_framework', 'corsheaders']:
        continue

    app_path = os.path.join(BASE_DIR, app)

    # Find each app's confing file, conbine
    if 'config.py' in os.listdir(app_path):
        config_file = importlib.import_module('{}.config'.format(app))

        # Get Contributor List
        if hasattr(config_file, '__CONTRIBUTORS__'):
            contributors = getattr(config_file, '__CONTRIBUTORS__')
            for member in contributors:
                if member not in __CONTRIBUTORS__:
                    __CONTRIBUTORS__.append(member)

        # Get App Version
        if hasattr(config_file, '__API_VERSION__'):
            app_version = getattr(config_file, '__API_VERSION__')
            for v in app_version:
                __API_VERSION__ |= set(['{}/{}'.format(app, v)])

    # Find cron jobs and append into main `CRONJOBS` to run the scheduled commands
    if 'cron.py' in os.listdir(app_path):
        cron_file = importlib.import_module('{}.cron'.format(app))
        if hasattr(cron_file, 'CRON_JOBS'):
            cron_jobs = getattr(cron_file, 'CRON_JOBS')
            for cron in cron_jobs:
                if cron not in CRONJOBS:
                    CRONJOBS.append(cron)
