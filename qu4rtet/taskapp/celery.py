import os
import logging
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings
import celery.signals
logger = logging.getLogger(__name__)

@celery.signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    print('on_celery_setup_logging signal hadled.')
    pass


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'config.settings.production')  # pragma: no cover
    print('Using production settings.')
    print(settings.__dict__)

logger.info('Using settings module %s', os.environ['DJANGO_SETTINGS_MODULE'])
logger.info('Using database at %s', os.environ['DATABASE_HOST'])

app = Celery('qu4rtet')



class CeleryConfig(AppConfig):
    name = 'qu4rtet.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        logger.info('Loading the celery app...')
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks(force=True)
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        if getattr(settings, 'USE_SENTRY', False) == True:
            # should be defined in production only
            from raven import Client as RavenClient
            from raven.contrib.celery import \
                register_signal as raven_register_signal
            from raven.contrib.celery import \
                register_logger_signal as raven_register_logger_signal

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['DSN'])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)
