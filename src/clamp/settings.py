"""
Django settings for clamp project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import ldap
from os import environ
from pathlib import Path
from json import load
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = True
DEBUG = bool(int(environ.get('DEBUG')))

# ALLOWED_HOSTS= ['*',]
ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS').split()
_ = [
        [
            f'{proto}{host}' for proto in ['http://', 'https://']
        ] for host in ALLOWED_HOSTS
    ]
CSRF_TRUSTED_ORIGINS = [item for i in _ for item in i]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'channels',

    'notification',
    'dashboard',
    'naumen',

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

ROOT_URLCONF = 'clamp.urls'

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

WSGI_APPLICATION = 'clamp.wsgi.application'
ASGI_APPLICATION = 'clamp.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':  environ.get('SQL_ENGINE'),
        'HOST': environ.get('SQL_HOST'),
        'PORT': int(environ.get('SQL_PORT')),
        'USER': environ.get('SQL_USER'),
        'PASSWORD': environ.get('SQL_PASSWORD'),
        'NAME': environ.get('SQL_NAME'),
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
    },
}

# LDAP
LDAP_CUSTOMER_NAME = 'CN=' + environ.get('LDAP_SERVER_CN')
LDAP_ORGANIZATIONAL_UNIT = 'OU=' + ',OU='.join(
    environ.get('LDAP_SERVER_OU').split(','))
LDAP_DOMAIN_COMPONENT = 'DC=' + ',DC='.join(
    environ.get('LDAP_SERVER_DC').split(','))

AUTH_LDAP_AUTHORIZE_ALL_USERS = True
AUTH_LDAP_PERMIT_EMPTY_PASSWORD = False
AUTH_LDAP_SERVER_URI = environ.get('LDAP_SERVER_URI')

AUTH_LDAP_BIND_DN = (f'{LDAP_CUSTOMER_NAME},' + f'{LDAP_ORGANIZATIONAL_UNIT},'
                     + f'{LDAP_DOMAIN_COMPONENT}')
AUTH_LDAP_BIND_PASSWORD = environ.get('NAUMEN_PASSWORD')

AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_DOMAIN_COMPONENT, ldap.SCOPE_SUBTREE,
                                   "(sAMAccountName=%(user)s)")

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LDAP_DOMAIN_COMPONENT,
                                    ldap.SCOPE_SUBTREE, "(objectClass=group)"
                                    )
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="CN")

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_staff": environ.get('LDAP_SERVER_ADMIN'),
    "is_superuser": environ.get('LDAP_SERVER_ADMIN'),
}

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

# Authentication backends

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.' +
        'password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.' +
        'password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.' +
        'password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.' +
        'password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = '/static/'
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = "redis://redis:6379/0"

CELERY_RESULT_BACKEND = 'django-db'

CELERY_CACHE_BACKEND = 'django-cache'

NAUMEN_LOGIN = environ.get('NAUMEN_LOGIN')

NAUMEN_PASSWORD = environ.get('NAUMEN_PASSWORD')

NAUMEN_DOMAIN = environ.get('NAUMEN_DOMAIN')

with open('config.json') as naumen_settings:
    NAUMEN_URL = load(naumen_settings)['url']

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ['redis://redis:6379/2'],
        }
    }
}
