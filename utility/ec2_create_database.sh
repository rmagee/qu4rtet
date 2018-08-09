#!/usr/bin/env bash
/home/ubuntu/.virtualenvs/qu4rtet/bin/python manage.py create_database
echo "Performing migrations..."
/home/ubuntu/.virtualenvs/qu4rtet/bin/python manage.py migrate --no-input
/home/ubuntu/.virtualenvs/qu4rtet/bin/python manage.py migrate --no-input --run-syncdb
echo "Creating superuser..."
/home/ubuntu/.virtualenvs/qu4rtet/bin/python manage.py create_super_from_env --no-input --run-syncdb
echo "Complete."
