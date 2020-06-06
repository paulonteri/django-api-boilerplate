from backend.settings.base import *

SECRET_KEY = '6h03)d($%+c4r#p65#ctnk3*u21^v@q+*e^ue0+llrq%zv(94z'

DEBUG = False

ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',  # Or path to database file if using sqlite3.
        'USER': 'myuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',  # Set to empty string for default.
    }
}

# django-cors-headers
CORS_ORIGIN_WHITELIST = ['http://example.com', 'https://example.com']

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        ('knox.auth.TokenAuthentication',),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ]
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
