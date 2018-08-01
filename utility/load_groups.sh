#!/usr/bin/env bash

python manage.py create_capture_groups
python manage.py create_epcis_groups
python manage.py create_masterdata_groups
python manage.py create_output_groups
python manage.py load_serialbox_auth
python manage.py load_random_flavorpack_auth

