# assumes you set up using the ubuntu/debian setup instructions
sudo supervisorctl stop guni:gunicorn
sudo supervisorctl start guni:gunicorn
sudo supervisorctl stop flower
sudo supervisorctl start flower
sudo systemctl restart nginx
sudo /etc/init.d/celeryd stop
sudo /etc/init.d/celeryd start
