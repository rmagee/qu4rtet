#!/usr/bin/env bash
workon qu4rtet
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py load_output_rules
. utility/load_groups.sh
