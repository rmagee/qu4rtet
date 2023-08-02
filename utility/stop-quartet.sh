#!/usr/bin/env bash
sudo systemctl stop gunicorn.socket
sudo systemctl stop gunicorn.service
sudo systemctl stop nginx
sudo systemctl stop celery.service
sudo systemctl stop flower.service

