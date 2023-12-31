#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace
pip install -r ../../requirements/local.txt
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver_plus 0.0.0.0:8000
echo "CREATING superuser..."
echo "from django.contrib.auth.models import User; User.objects.filter(email='${POSTGRES_USER}@qu4rtet.local').delete(); User.objects.create_superuser('${POSTGRES_USER}', '${POSTGRES_USER}@qu4rtet.local', '${POSTGRES_PASSWORD}')" | python manage.py shell
