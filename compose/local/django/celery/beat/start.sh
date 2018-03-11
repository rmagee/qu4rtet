#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace


rm -f './celerybeat.pid'
celery -A qu4rtet.taskapp beat -l INFO
