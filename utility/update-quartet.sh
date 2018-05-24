#!/usr/bin/env bash

cd /srv/qu4rtet
git stash
git checkout master
git pull https://gitlab.com/serial-lab/qu4rtet.git master
git fetch --tags
export LATESTQ4=`git describe --abbrev=0 --tags`
git checkout tags/$LATESTQ4
sudo pip3 install -r ./requirements/production.txt
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py migrate --run-syncdb
sudo python3 manage.py collectstatic
sudo pip3 install eparsecis --upgrade
sudo pip3 install epcpyyes --upgrade
sudo pip3 install quartet_capture --upgrade
sudo pip3 install quartet_epcis --upgrade
sudo pip3 install serialbox --upgrade
sudo pip3 install random_flavorpack --upgrade
sudo pip3 install quartet_manifest --upgrade
sudo pip3 install quartet_masterdata --upgrade
sudo restart-quartet
