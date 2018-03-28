"""
Local settings for QU4RTET project.

- Run in Debug mode

- Use mailhog for emails via Docker

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=False)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
print('Debug set to: %s' % env.bool('DJANGO_DEBUG', True))
# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='gLvAMdTEIWtTHVHTcAfivd0loFluxWtBez3Hy72TRqJ2qeit59')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = env('EMAIL_HOST', default='localhost')

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

import socket
import os

# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# django admin
# -----------------------------------------------------------------------------
INSTALLED_APPS += ['django_admin_bootstrapped', 'django.contrib.admin']

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = env.bool('CELERY_ALWAYS_EAGER', True)
########## END CELERY

# When not running in debug mode
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost'])

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
import logging

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()]
)

pil_logger = logging.getLogger('PIL.Image')
pil_logger.setLevel(logging.INFO)

# allow restful registration API endpoints
ENABLE_REGISTRATION = False
