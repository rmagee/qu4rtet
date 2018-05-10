#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace


export DJANGO_SETTINGS_MODULE=config.settings.local
celery -A qu4rtet.taskapp worker -l INFO
flower -A qu4rtet.taskapp --port=5555

