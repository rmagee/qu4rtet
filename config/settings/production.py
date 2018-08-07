"""
Production settings for QU4RTET project.


- Use Amazon's S3 for storing static files and uploaded media
- Use mailgun to send emails

- Use sentry for error logging


- Use opbeat for error reporting

"""

import logging
import os
from .base import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

USE_SENTRY = env.bool('USE_SENTRY', False)
USE_ELASTIC_APM = env.bool('USE_ELASTIC_APM', False)

if USE_SENTRY:
    # raven sentry client
    # See https://docs.sentry.io/clients/python/integrations/django/
    INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]
    RAVEN_MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']
    MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

if USE_ELASTIC_APM:
    INSTALLED_APPS += ['elasticapm.contrib.django', ]
    ELASTIC_APM = {
        'SERVICE_NAME': env('ELASTIC_APM_SERVICE_NAME'),
        'SECRET_TOKEN': env('ELASTIC_APM_SECRET_TOKEN'),
        'SERVER_URL': env('ELASTIC_APM_SERVER_URL')
    }
    MIDDLEWARE = [
                     'elasticapm.contrib.django.middleware.TracingMiddleware',
                 ] + MIDDLEWARE

if env.bool('HTTPS_ONLY', True):
    from .secure import *

CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS',
                         default=['localhost'])
# END SITE CONFIGURATION

INSTALLED_APPS += ['gunicorn', ]

# if aws is not configured, local file storage will be used
if env.bool('USE_AWS', default=False):
    # STORAGE CONFIGURATION
    # ------------------------------------------------------------------------------
    # Uploaded Media Files
    # ------------------------
    # See: http://django-storages.readthedocs.io/en/latest/index.html
    INSTALLED_APPS += ['storages', ]
    AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIRY = 60 * 60 * 24 * 7

    # TODO See: https://github.com/jschneier/django-storages/issues/47
    # Revert the following and use str after the above-mentioned bug is fixed in
    # either django-storage-redux or boto
    control = 'max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': bytes(control, encoding='latin-1'),
    }

    # URL that handles the media served from MEDIA_ROOT, used for managing
    # stored files.

    #  See:http://stackoverflow.com/questions/10390244/
    from storages.backends.s3boto3 import S3Boto3Storage

    StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')  # noqa
    MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='media',
                                                    file_overwrite=False)  # noqa
    DEFAULT_FILE_STORAGE = 'config.settings.production.MediaRootS3BotoStorage'

    MEDIA_URL = 'https://s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME

    # Static Assets
    # ------------------------

    STATIC_URL = 'https://s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
    STATICFILES_STORAGE = 'config.settings.production.StaticRootS3BotoStorage'
    # See: https://github.com/antonagestam/collectfast
    # For Django 1.7+, 'collectfast' should come before
    # 'django.contrib.staticfiles'
    AWS_PRELOAD_METADATA = True
    INSTALLED_APPS += ['collectfast', ]

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='QU4RTET <noreply@serial-lab.local>')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[QU4RTET]')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Uncomment for Anymail with Mailgun
# INSTALLED_APPS += ['anymail', ]
# ANYMAIL = {
#     'MAILGUN_API_KEY': env('DJANGO_MAILGUN_API_KEY'),
#     'MAILGUN_SENDER_DOMAIN': env('MAILGUN_SENDER_DOMAIN')
# }
# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Use the Heroku-style specification
# DATABASE CONFIGURATION
docker = env.bool('DOCKER', False)
if not docker:
    database_host = env.str('DATABASE_HOST')
else:
    database_host = env.str('DOCKER_DATABASE_HOST')

default_db_url = "postgres://{0}:{1}@{2}:5432/{3}".format(
    env.str('POSTGRES_USER'),
    env.str('POSTGRES_PASSWORD'),
    database_host,
    env.str('POSTGRES_DB')
)
DATABASES = {'default': env.db('DATABASE_URL', default_db_url)}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Sentry Configuration
if USE_SENTRY:
    SENTRY_DSN = env('DJANGO_SENTRY_DSN')
    SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT',
                        default='raven.contrib.django.raven_compat.DjangoClient')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry', ],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console', ],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console', ],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console', ],
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': ['console', 'sentry', ],
                'propagate': False,
            },
        },
    }
    SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
    RAVEN_CONFIG = {
        'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
        'DSN': SENTRY_DSN
    }
else:
    CELERYD_HIJACK_ROOT_LOGGER = False
    # get the logging path from the .env file
    LOGGING_PATH = env.str('LOGGING_PATH', '/var/log/quartet')
    file_path = os.path.join(LOGGING_PATH, 'quartet.log')
    print('Logging to path %s' % file_path)
    # check to make sure that there are write rights to the log location
    if not os.access(LOGGING_PATH, os.W_OK):
        raise IOError('Logging is configured for a path (%s) which QU4RTET '
                      'does not currently have rights to write too.  The '
                      'account which needs these rights is typically that '
                      'of the web server or process running the celery '
                      'daemon.')
    print('Logging rights are confirmed.')
    LOGGING_LEVEL=env.str('LOGGING_LEVEL', 'WARNING')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': LOGGING_LEVEL,
            'handlers': ['file', ],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': LOGGING_LEVEL,
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': file_path,
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
            'celery': {
                'handlers': ['file'],
                'level': LOGGING_LEVEL,
                'propagate': False
            },
            'celery.task': {
                'handlers': ['file'],
                'level': LOGGING_LEVEL,
                'propagate': False
            }
        },
    }

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
if env.bool('DJANGO_ENABLE_ADMIN', False):
    INSTALLED_APPS += ['django.contrib.admin']
