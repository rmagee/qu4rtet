#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace


celery -A qu4rtet.taskapp worker -l INFO
