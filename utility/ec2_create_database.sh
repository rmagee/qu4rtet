#!/usr/bin/env bash
echo "Importing environment variables"
set -o allexport; source /tmp/q4_env; set +o allexport
echo "Creating the quartet database..."
POSTGRES_PORT=${POSTGRES_PORT:=5432}
echo "Postgres Port=$POSTGRES_PORT"
createdb -e -E UTF8 -O $POSTGRES_USER -U $POSTGRES_USER --host=$DATABASE_HOST --port=$POSTGRES_PORT $POSTGRES_DB 'The QU4RTET database backend.'
echo "Running migrations..."
python manage.py migrate
