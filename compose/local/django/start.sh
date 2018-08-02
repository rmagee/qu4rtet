#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

echo "RUNNING makemigrations..."
python manage.py makemigrations
echo "RUNNING migrage..."
python manage.py migrate --run-syncdb
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver_plus 0.0.0.0:8000
echo "CREATING superuser..."
echo "from django.contrib.auth.models import User; User.objects.filter(email='${POSTGRES_USER}@qu4rtet.local').delete(); User.objects.create_superuser('${POSTGRES_USER}', '${POSTGRES_USER}@qu4rtet.local', '${POSTGRES_PASSWORD}')" | python manage.py shell
