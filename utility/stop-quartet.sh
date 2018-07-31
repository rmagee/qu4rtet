sudo supervisorctl stop guni:gunicorn
sudo systemctl stop nginx
sudo /etc/init.d/celeryd stop
sudo supervisorctl stop flower

