# Docker

QU4RTET has two docker-compose scripts in the root directory of the project 
that allow you to deploy the application framework for both production and
for local development, testing and sandbox instances, for example. 

## The Setup
There are two docker compose files in the root of the QU4RTET project.  

    production.yml
    localy.yml
    
## What you need

### Docker Command Line Tools
Obviously you will need the latest docker and docker-compose binaries for your
platform.  You can download [Docker here.](https://docker.com)

### QU4RTET Source Code
You can download the QU4RTET source code or clone it using git [at the 
SerialLab Gitlab page.](https://gitlab.com/serial-lab/qu4rtet).

### Production Containers

The docker-compose stack (for production) is composed of the following:

* `NGINX` - running the web server/reverse proxy.
* `Gunicorn/Django` - The QU4RTET API running behind `Gunicorn`
* `Celery` - The celery worker handles the async processing of QU4RTET tasks.  This
shares the same image as the `Guincorn/Django`
* `RabbitMQ` - The task broker for `Celery` 
* `PostgreSQL` - The database layer for the application.


## Local Containers

The technology stack is the same as production, however, there is no NGINX 
layer and postgres and celery all reside on the same instance as the application
so those three containers above are consolidated.  

## Launching

To launch the production stack, navigate to the root of the QU4RTET source 
directory and execute the following (substitute `local.yml` if you are 
looking to run a development environment:

    docker-compose -f production.yml build
    docker-compose -f production.yml up -d
    docker-compose -f production.yml run -u 0 --rm django /bin/bash
    python manage.py migrate
    python manage.py collectstatic --no-input
    . utility/load_example_data.sh
    python manage.py createsuperuser 
    # follow the prompts
    exit
  
## Testing the Launch

The environment will load to port 80 for HTTP for the `production` build
and to port 8000 for the `local` build.

### Acess the API Page

If your system is running correctly you should be able to access the
API pages via the following links

http://localhost

or for local.yml

http://localhost:8000

### Install QU4RTET UI

If everything is working correctly you are good to go.  [Download
QU4RTET UI](https://gitlab.com/serial-lab/quartet-ui) and, if you'd like
to upload some test EPCIS files you can 
[grab some here.](https://gitlab.com/serial-lab/quartet_epcis/tree/master/tests/data) 

## Notes

### HTTPS is NOT enabled by default.

Since we can't provide you with certificates for your own domains, the
QU4RTET docker NGINX instance does not have a certificate installed to 
enable HTTPS. If you'd like to use `certbot` and `let's encrypt` there is a
a script in the `utility` directory named `enable-https.sh` that you
can utilize.  Otherwise, you will have to follow the NGINX documentation 
for securing the web server.
