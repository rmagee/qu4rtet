
import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('qu4rtet')

class CeleryConfig(AppConfig):
    name = 'qu4rtet.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks(force=True)
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        if hasattr(settings, 'RAVEN_CONFIG'):
            # Celery signal registration
            # Since raven is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal as raven_register_signal
            from raven.contrib.celery import register_logger_signal as raven_register_logger_signal

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['DSN'])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)

        if hasattr(settings, 'OPBEAT'):
            # Since opbeat is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            from opbeat.contrib.django.models import client as opbeat_client
            from opbeat.contrib.django.models import logger as opbeat_logger
            from opbeat.contrib.django.models import register_handlers as opbeat_register_handlers
            from opbeat.contrib.celery import register_signal as opbeat_register_signal

            try:
                opbeat_register_signal(opbeat_client)
            except Exception as e:
                opbeat_logger.exception('Failed installing celery hook: %s' % e)

            if 'opbeat.contrib.django' in settings.INSTALLED_APPS:
                opbeat_register_handlers()
