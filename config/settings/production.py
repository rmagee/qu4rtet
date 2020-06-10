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

USE_SENTRY = env.bool('USE_SENTRY', False)
USE_ELASTIC_APM = env.bool('USE_ELASTIC_APM', False)

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
if os.environ.get('USE_DOCKER') == 'yes':
    SESSION_COOKIE_SECURE = False

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
    # Uploaded Task Files
    # ------------------------
    # See: http://django-storages.readthedocs.io/en/latest/index.html
    INSTALLED_APPS += ['storages', ]
    AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY', None)
    AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIRY = 60 * 60 * 24 * 7
    control = 'max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': control,
    }
    from storages.backends.s3boto3 import S3Boto3Storage
    MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='media',
                                                    file_overwrite=False)
    DEFAULT_FILE_STORAGE = 'config.settings.production.MediaRootS3BotoStorage'
    MEDIA_URL = 'https://s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
    AWS_PRELOAD_METADATA = True


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

# Sentry Configuration
if USE_SENTRY:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env('DJANGO_SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )
else:
    CELERYD_HIJACK_ROOT_LOGGER = False
    # get the logging path from the .env file
    LOGGING_PATH = env.str('LOGGING_PATH', '/tmp')
    file_path = os.path.join(LOGGING_PATH, 'quartet.log')
    print('Logging to path %s' % file_path)
    # check to make sure that there are write rights to the log location
    if not os.access(LOGGING_PATH, os.W_OK):
        raise IOError('Logging is configured for a path (%s) which QU4RTET '
                      'does not currently have rights to write too.  The '
                      'account which needs these rights is typically that '
                      'of the web server or process running the celery '
                      'daemon.' % file_path)
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
                          '%(process)d %(thread)d %(funcName)s %(lineno)d '
                          '%(message)s'
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
if env.bool('DJANGO_ENABLE_ADMIN', True):
    INSTALLED_APPS += ['django.contrib.admin']

logging.info('Default database host: %s', database_host)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DATA_UPLOAD_MAX_MEMORY_SIZE=6553600
FILE_UPLOAD_MAX_MEMORY_SIZE=6553600

try:
    from config.settings.local_settings import *
    print('LOCAL SETTINGS FOUND')
except ImportError:
    print('No local settings detected.')
