#!/bin/sh

set -o errexit
set -o nounset


celery -A qu4rtet.taskapp beat -l INFO
