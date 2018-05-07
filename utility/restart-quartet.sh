# assumes you set up using the ubuntu/debian setup instructions
sudo supervisorctl stop all
sudo supervisorctl start all
sudo systemctl restart nginx
sudo /etc/init.d/celeryd stop
sudo /etc/init.d/celeryd start
