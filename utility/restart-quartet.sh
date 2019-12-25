#!/usr/bin/env bash
# assumes you set up using the ubuntu/debian setup instructions
#!/usr/bin/env bash
# assumes you set up using the ubuntu/debian setup instructions
sudo systemctl restart gunicorn.socket
sudo systemctl restart gunicorn.service
sudo systemctl restart flower.service
sudo systemctl restart nginx
sudo systemctl restart celery.service
sudo systemctl status celery nginx flower gunicorn

