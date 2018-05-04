Ubuntu/Debian Installation
==========================

Install Requirements
--------------------

.. code-block::text

    sudo apt-get -y install update
    sudo apt-get -y install rabbitmq-server python3-pip postgresql postgresql-contrib gunicorn nginx supervisor
    cd /srv
    sudo git clone https://gitlab.com/serial-lab/qu4rtet.git
    sudo chown -R qu4rtet:root qu4rtet/
    cd qu4rtet
    # for production
    sudo pip3 install -r requirements/production.txt
    # for running the dev server local, uncomment out below and/or execute
    # on the command line:
    # sudo pip3 install -r requirements/local.txt


Configure Database
------------------

This example is for PostgreSQL.  If you are using another database as a back-end
(which is fine) you'll need to configure it accordingly.

.. code-block::text

Switch over to the postgres user.

.. code-block::text

    sudo -i -u postgres

Now launch psql and create a password for the postgres user.  The default
postgres account has a secret password.  Change it to something secure
that you can remember.

.. code-block::text
    psql
    # now IN psql execute the following to change the passwords
    \password postgres

Next.  Hit ctrl+d to exit psql.

Now we are going to create the database for QU4RTET along with the default
user account that QU4RTET will use to access the database.

**NOTE: If you are configuring a remote database backend on another host,
make sure to change the `host` parameters below!**

.. code-block::text

    # create quartet user and database
    createuser -P -d -l -r -S -i --replication --host=localhost --port=5432 qu4rtet
    createdb -e -E UTF8 -O qu4rtet --host=localhost --port=5432  qu4rtet 'The QU4RTET database backend.'


Create an .env File
-------------------
In the root directory of QU4RTET execute the following:

.. code-block::text

    sudo touch .env
    sudo nano .env

Now you are in the `.env` file.  This is where QU4RTET will read much of
it's configuration info from.  Enter in the following data.  **Do not forget
to put in the password of the qu4rtet user that you created in the steps
above under the POSTGRES_PASSWORD configuration value!!!...in addition,
if you are using a different database host make sure to change the host
and port values below as well!!!**

Paste the following configuration into the .env file and modify accordingly
where it says ## CHANGE THIS ... ##.

You will most likely only change the `POSTGRES_PASSWORD` and
`DJANGO_SECRET_KEY` values.  You can generate a new secret key value here:
https://www.miniwebtool.com/django-secret-key-generator/

.. code-block::text

    # postgres config
    POSTGRES_DB=qu4rtet
    POSTGRES_USER=qu4rtet
    POSTGRES_PORT=5432
    # the password should be the password you configured in the database
    # step in the instructions above.
    # for example POSTGRES_PASSWORD=mysecurepassword
    POSTGRES_PASSWORD=## CHANGE THIS ##

    DATABASE_HOST=localhost
    DOCKER_DATABASE_HOST=postgres # for use with docker compose- do not change

    CONN_MAX_AGE=60

    # General settings
    DJANGO_SETTINGS_MODULE=config.settings.production
    # Generate a new secret key here: https://www.miniwebtool.com/django-secret-key-generator/
    DJANGO_SECRET_KEY=## CHANGE THIS - generate a new secret key ##
    DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
    DJANGO_DEBUG=False

    # AWS Settings if you want to use S3 file storage as the default
    # file storage backend configure this.
    USE_AWS=False
    DJANGO_AWS_ACCESS_KEY_ID=
    DJANGO_AWS_SECRET_ACCESS_KEY=
    DJANGO_AWS_STORAGE_BUCKET_NAME=

    # Used with https://www.mailgun.com/ email server
    DJANGO_MAILGUN_API_KEY=
    DJANGO_SERVER_EMAIL=
    MAILGUN_SENDER_DOMAIN=

    # Security! Better to use DNS for this task, but you can use redirect
    DJANGO_SECURE_SSL_REDIRECT=False

    # django-allauth
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=False
    # Sentry
    USE_SENTRY=False
    DJANGO_SENTRY_DSN=

    USE_OPBEAT=False
    DJANGO_OPBEAT_ORGANIZATION_ID=
    DJANGO_OPBEAT_APP_ID=
    DJANGO_OPBEAT_SECRET_TOKEN=

    # change me if the celery broker is redis or is on a different server
    # this is configured for a local RabbitMQ
    CELERY_BROKER_URL="amqp://guest@localhost//"

Save the file and exit.

Run The QU4RTET Database Migrations
-----------------------------------

The steps below will populate the `qu4rtet` database created above with
all of the tables and other logic necessary to support the application.

First switch out of the postgres user account by typing exit:

.. code-block::text

    exit

.. code-block::text

    sudo python3 manage.py makemigrations
    python3 manage.py migrate --run-syncdb
    python3 manage.py migrate
    python3 manage.py collectstatic --no-input
    python3 manage.py createsuperuser

Run The Dev Server
------------------

A quick test of the configuration is to run the dev server as below.

.. code-block::

    python3 manage.py runserver

If it runs without error we are good for now.  Kill the test server with a
`CTRL+C` and we will move on.


Configure Celery Worker to Run as Daemon
----------------------------------------
QU4RTET uses the Celery Task Queue (http://www.celeryproject.org/) to
distribute out work among multiple computers/containers, etc. should that
be necessary.  Here we are just going to ensure that the local celery
daemon is up and running.  For more sophisticated Celery deployments
see the Celery documentation.

Here we are going to download the recommended daemon script from the
celery github repostory and then configure it for local use.

.. code-block::

    # switch directories
    cd /etc/init.d
    # download the file
    sudo wget https://raw.githubusercontent.com/celery/celery/master/extra/generic-init.d/celeryd celeryd
    # grant execution rights
    sudo chmod ugo+x celeryd
    # switch directories
    cd /etc/default
    # create a celery config file
    sudo touch celeryd
    # open with editor
    sudo nano celeryd

Next you will paste in the following configuration which is meant to work
with all of the steps you've followed thus far.  If you've deviated from
all of the steps above you may experience errors in your system.

.. code-block::

    # here we start five celery nodes
    CELERYD_NODES="qu4ret_worker_1 qu4rtet_worker2 qu4rtet_worker3 qu4rtet_worker4 qu4rtet_worker5"

    # Absolute or relative path to the 'celery' command:
    CELERY_BIN="/usr/local/bin/celery"

    # App instance to use
    CELERY_APP="qu4rtet.taskapp.celery:app"

    # Where to chdir at start.
    CELERYD_CHDIR="/srv/qu4rtet"

    # Extra command-line arguments to the worker
    CELERYD_OPTS="--time-limit=300 --concurrency=8"

    # Only set logging level to DEBUG if you're having problems
    #CELERYD_LOG_LEVEL="DEBUG"

    # %n will be replaced with the first part of the nodename.
    CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
    CELERYD_PID_FILE="/var/run/celery/%n.pid"

    # Workers should run as an unprivileged user.
    #   You need to create this user manually (or you can choose
    #   a user/group combination that already exists (e.g., nobody).
    CELERYD_USER="celery"
    CELERYD_GROUP="celery"

    # If enabled pid and log directories will be created if missing,
    # and owned by the userid/group configured.
    CELERY_CREATE_DIRS=1


Save the file and exit.  Next, create the celery user and give it a secure
password that you will remember.

.. code-block::text

    sudo adduser celery

Next, see if you can start celery.

.. code-block::text

    sudo /etc/init.d/celeryd start
    sudo /etc/init.d/celeryd status

At this point you should be ready to configure the web server.


Quickly Test Gunicorn
---------------------
Hop into the qu4rtet directory and see if you can run gunicorn without issue.

.. code-block::text

    cd /srv/qu4rtet
    sudo gunicorn --bind 0.0.0.0:8000 config.wsgi:application

It should start without error.  Hit CTRL+C to stop the gunicorn server.


Create a Gunicorn Supervisor File
---------------------------------
Here we will daemonize Gunicorn with supervisor (which will also
monitor the process).

.. code-block::text

    sudo nano /etc/supervisor/conf.d/gunicorn.conf

Then paste the following into nano:

.. code-block::text

    [program:gunicorn]
    directory=/srv/qu4rtet
    command=gunicorn --workers 3 --bind unix:/srv/qu4rtet/qu4rtet.sock config.wsgi:application
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/gunicorn/gunicorn.out.log
    stdout_logfile=/var/log/gunicorn/gunicorn.err.log
    user=root
    group=www-data
    environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8

    [group:guni]
    programs:gunicorn

Check to make sure gunicorn is running qu4rtet:

.. code-block::text

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status

Configure Nginx
---------------
In the utils directory of the qu4rtet directory there is a pre-configured
nginx file.  Copy that file to the nginx directory and then edit it by changing
the `server_name` field from SERVER_DOMAIN_OR_IP to whatever your host name
or server ip address is.  ** Remember to make sure that whatever your
host name is, it is also configured in the .env file under `DJANGO_ALLOWED_HOSTS`
or your static files will not be served by nginx.**

.. code-block::text

    # copy the config file from the qu4rtet folder
    sudo cp utility/nginx.conf /etc/nginx/sites-available/qu4rtet
    # edit
    sudo nano /etc/ng


For example:

.. code-block::text

    server {
        listen 80;
        server_name serial-lab.local;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /srv/qu4rtet;
        }
        location / {
            include proxy_params;
            proxy_pass http://unix:/srv/qu4rtet/qu4rtet.sock;
        }
    }

Now create a symlink in the sites-enabled directory of nginx.

.. code-block::text

    sudo ln -s /etc/nginx/sites-available/qu4rtet /etc/nginx/sites-enabled
    # test the config
    sudo nginx -t
    # restart the server
    sudo systemctl restart nginx

Check the Site
--------------
Your server should be up and running now.  Navigate to it in your browser.
If you have any questions, reach out to us.  Our contact info, slack-channel
and such is available at http://serial-lab.com

Comments / Issues
-----------------
If you find any errors with this documentation.  Please feel free to create
an issue on our gitlab page at:

https://gitlab.com/serial-lab/qu4rtet/issues
