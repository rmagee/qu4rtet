#!/usr/bin/env bash
echo "Importing environment variables"
set -o allexport; source /tmp/q4_env; set +o allexport
echo "Creating the quartet database..."
sudo su postgres
POSTGRES_PORT=${POSTGRES_PORT:=5432}
echo "Postgres Port=$POSTGRES_PORT"
createdb -e -E UTF8 -O $POSTGRES_USER -U $POSTGRES_USER --host=$DATABASE_HOST --port=$POSTGRES_PORT $POSTGRES_DB 'The QU4RTET database backend.'
exit
echo "Running migrations..."
/home/ubuntu/.virtualenvs/qu4rtet/bin/python manage.py migrate --no-input
/home/ubuntu/.virtualenvs/qu4rtet/bin/python manage.py migrate --no-input --run-syncdb
echo "Creatging superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser(\"$DJANGO_SUPERUSER\", \"$DJANGO_SUPERUSER_EMAIL\", \"$DJANGO_SUPERUSER_PASSWORD\")" | /home/ubuntu/.virtualenvs/qu4rtet/bin/python manage.py shell
