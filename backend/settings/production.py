from backend.settings.base import *

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG')
TESTING = env.bool('TESTING', False)

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
        'CONN_MAX_AGE': env.int('DB_CONN_MAX_AGE', 0),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_debug_false': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_debug_false', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

SENTRY_ACTIVE = False
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        environment=os.environ.get('SENTRY_ENVIRONMENT', 'production'),
    )
    SENTRY_ACTIVE = True

# Django Query Count (Only works with Debug=True)
# https://github.com/bradmontgomery/django-querycount
if TESTING:
    QUERYCOUNT = {
        'THRESHOLDS': {
            'MEDIUM': 50,
            'HIGH': 200,
            'MIN_TIME_TO_LOG': 0,
            'MIN_QUERY_COUNT_TO_LOG': 0
        },
        'IGNORE_REQUEST_PATTERNS': [],
        'IGNORE_SQL_PATTERNS': [],
        'DISPLAY_DUPLICATES': 10,
        'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
    }

    MIDDLEWARE += [
        'querycount.middleware.QueryCountMiddleware',
    ]

# Django Cacheops
# https://github.com/Suor/django-cacheops
if os.environ.get('CACHE_HOST'):
    CACHEOPS_PREFIX = lambda _: env("CACHEOPS_PREFIX")

    CACHEOPS_REDIS = {
        'host': env('CACHE_HOST'),
        'port': env.int('CACHE_PORT'),
        # 'db': env('CACHE_DB'),
        'password': env('CACHE_PASSWORD'),
        'socket_timeout': 3,
    }

    CACHEOPS_DEGRADE_ON_FAILURE = True

    CACHE_MINUTES = int(os.environ.setdefault('CACHE_MINUTES', '10080'))
    CACHE_MINUTES_LONGER = int(os.environ.setdefault('CACHE_MINUTES_LONGER', '87600'))

    # cacheops settings
    # https://github.com/Suor/django-cacheops#setup
    CACHEOPS = {
        'accounts.*': {'ops': {'fetch', 'get'}, 'timeout': 60 * 60},
        # 'app_name.*': {'ops': 'all', 'timeout': 60 * CACHE_MINUTES},
        # 'products.*': {'ops': 'all', 'timeout': 60 * CACHE_MINUTES_LONGER},
        # 'name_app.*': None,
    }

    if DEBUG or TESTING:
        from cacheops.signals import cache_read


        def stats_collector(sender, func, hit, **kwargs):
            event = 'hit' if hit else 'miss'
            print(event)
            print(func)


        cache_read.connect(stats_collector)
