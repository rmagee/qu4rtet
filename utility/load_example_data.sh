#!/usr/bin/env bash
python manage.py md_test_data
python manage.py load_output_rules
python manage.py load_test_random_pools
python manage.py load_test_pools
