#!/usr/bin/env bash

cd /srv/qu4rtet
git pull
export LATESTQ4=`git describe --abbrev=0 --tags`
git checkout tags/$LATESTQ4
sudo pip3 install -r ./requirements/production.txt
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py migrate --run-syncdb
sudo python3 manage.py collectstatic
sudo restart-quartet
