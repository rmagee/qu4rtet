#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

export DJANGO_SETTINGS_MODULE=config.settings.local
rm -f './celerybeat.pid'
celery -A qu4rtet.taskapp beat -l INFO
