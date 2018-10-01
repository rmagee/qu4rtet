#!/usr/bin/env bash

cd /srv/qu4rtet
echo "Stashing any local changes..."
git stash
echo "Checking out the master branch..."
git checkout master
echo "Pulling the lastest tag..."
git pull https://gitlab.com/serial-lab/qu4rtet.git master
git fetch --tags
export LATESTQ4=`git describe --abbrev=0 --tags`
echo "Latest Tag: $LATESTQ4"
git checkout tags/$LATESTQ4
echo "Installing latest requirements..."
workon qu4rtet
pip install -r ./requirements/production.txt
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py collectstatic
echo "Restarting the QU4RTET infrastructure."
sudo restart-quartet
echo "Complete."
