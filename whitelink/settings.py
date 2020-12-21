from email.utils import getaddresses
from pathlib import Path

import dj_email_url
import environ

from app.firewall import BaseRuleUpdater, AzureRuleUpdater

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY', default='change_me_in_production')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Application definition

INSTALLED_APPS = [
    'app.apps.WhitelinkConfig',

    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'whitelink.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'whitelink.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3'),
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# E-mail settings

# I prefer dj-email-url over django-environ
email_config = dj_email_url.parse(env('EMAIL_URL', default='smtp://'))
vars().update(email_config)
# ADMINS=Full Name <email-with-name@example.com>,anotheremailwithoutname@example.com
ADMINS = getaddresses([env('ADMINS', default='')])


# The destination ports that will be allowed on the firewall rules
ALLOW_PORTS = env.list('ALLOW_PORTS', cast=int, default=[9736, 22023])

# The rule updater class to use, should be either 'base' (no-op) or 'azure'
RULE_UPDATER = env('RULE_UPDATER', default='base')

# Azure configuration used for updating the network security group
#
# See the AzureRuleUpdater class.
AZURE_TENANT_ID = env('AZURE_TENANT_ID', default='')
AZURE_CLIENT_ID = env('AZURE_CLIENT_ID', default='')
AZURE_CLIENT_SECRET = env('AZURE_CLIENT_SECRET', default='')
AZURE_SUBSCRIPTION_ID = env('AZURE_SUBSCRIPTION_ID', default='')
AZURE_RESOURCE_GROUP = env('AZURE_RESOURCE_GROUP', default='')
AZURE_NETWORK_SECURITY_GROUP = env('AZURE_NETWORK_SECURITY_GROUP', default='')
