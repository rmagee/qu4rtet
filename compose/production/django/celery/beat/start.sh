#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A qu4rtet.taskapp beat -l INFO
