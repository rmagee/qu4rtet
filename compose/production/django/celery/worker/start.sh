#!/bin/sh

set -o errexit
set -o nounset


celery -A qu4rtet.taskapp worker -l INFO
