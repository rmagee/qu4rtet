#!/usr/bin/env bash
createdb -e -E UTF8 -O $POSTGRES_USER -U $POSTGRES_USER --host=$DATABASE_HOST --port=$POSTGRES_PORT $POSTGRES_DB 'The QU4RTET database backend.'
