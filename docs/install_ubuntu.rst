Ubuntu/Debian Installation
==========================

Before You Begin
----------------
It is important to follow all of the recommended paths and commands in this
document.  Not doing so will result in much heartache and wasting of time.
Make sure to:

# Always copy and paste the commands as expressed in the doc.
# When an example says "change this setting", etc. make sure to change the setting.

Install The Requirements
------------------------
As you can see below, you will need a flavor of python3 and pip3 which may or may not be present on
your base installation of Debian or Ubuntu.  Installing Python and using the
setup tools is well documented and is beyond the scope of this document.  The pip
installation is included below.


.. code-block:: text

    sudo apt-get -y update
    sudo apt-get -y install rabbitmq-server python3-pip postgresql postgresql-contrib gunicorn nginx supervisor apache2-utils python3-dev
    sudo ln -s /usr/bin/pip3 /usr/bin/pip
    cd /srv
    sudo git clone https://gitlab.com/serial-lab/qu4rtet.git
    sudo chown -R qu4rtet:root qu4rtet/
    cd qu4rtet
    # for production
    sudo pip3 install -r requirements/production.txt
    # the local packages are not required but will make your life easier if
    # you have problems getting the system running
    sudo pip3 install -r requirements/local.txt
    sudo pip3 install celery-flower


Configure Database
------------------

This example is for PostgreSQL.  If you are using another database as a back-end
(which is fine) you'll need to configure it accordingly.

Switch over to the postgres user.

.. code-block:: text

    sudo -i -u postgres

Now launch psql and create a password for the postgres user.  The default
postgres account has a secret password.  Change it to something secure
that you can remember.

.. code-block:: text
    psql
    # now IN psql execute the following to change the passwords
    \password postgres

Next.  Hit ctrl+d to exit psql.

Now we are going to create the database for QU4RTET along with the default
user account that QU4RTET will use to access the database.

**NOTE: If you are configuring a remote database backend on another host,
make sure to change the `host` parameters below!**

.. code-block:: text

    # create quartet user and database
    createuser -P -d -l -r -S -i --replication --host=localhost --port=5432 qu4rtet
    createdb -e -E UTF8 -O qu4rtet --host=localhost --port=5432  qu4rtet 'The QU4RTET database backend.'


Create an .env File
-------------------
In the root directory of QU4RTET execute the following:

.. code-block:: text

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

.. code-block:: text

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
    ### Change Below ###
    DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1' ## add your server ip / host name here ###
    DJANGO_DEBUG=False
    DJANGO_MEDIA_ROOT=/var/quartet/media/
    DJANGO_MEDIA_URL=/media/

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

    USE_ELASTIC_APM=False
    ELASTIC_APM_SERVICE_NAME=
    ELASTIC_APM_SECRET_TOKEN=
    ELASTIC_APM_SERVER_URL=

    # change me if the celery broker is redis or is on a different server
    # this is configured for a local RabbitMQ
    CELERY_BROKER_URL="amqp://guest@localhost//"

    # set the log file to your preferred location
    LOGGING_PATH=/var/log/quartet
    HTTPS_ONLY=False

Save the file and exit.

Run The QU4RTET Database Migrations
-----------------------------------

The steps below will populate the `qu4rtet` database created above with
all of the tables and other logic necessary to support the application.
In addition, it will move any static files required for the QU4RTET API
pages into a single directory to be served up by the webserver.

First switch out of the postgres user account by typing exit:

.. code-block:: text

    exit

.. code-block:: text

    sudo python3 manage.py makemigrations
    sudo python3 manage.py migrate --run-syncdb
    sudo python3 manage.py migrate
    sudo python3 manage.py collectstatic --no-input
    sudo python3 manage.py createsuperuser

Run The Dev Server
------------------

A quick test of the configuration is to run the dev server as below.

.. code-block:: text

    sudo python3 manage.py runserver

If it runs without error we are good for now- even if it returns a 400 HTTP
status that's Ok.  Kill the test server with a
`CTRL+C` and we will move on.


Configure Celery Worker to Run as Daemon
----------------------------------------
QU4RTET uses the Celery Task Queue (http://www.celeryproject.org/) to
distribute out work among multiple computers/containers, etc. should that
be necessary.  Here we are just going to ensure that the local celery
daemon is up and running.  For more sophisticated Celery deployments
see the Celery documentation.

Here we are going to download the recommended daemon script from the
celery github repostory and then configure it for local use.  Then we will
paste the `celeryd` file from the `utilities` folder into the
`/etc/default/` directory, add the celery user to the system and
start the Celery workers.

.. code-block:: text

    # switch directories
    cd /etc/init.d
    # download the file
    sudo wget https://raw.githubusercontent.com/celery/celery/master/extra/generic-init.d/celeryd celeryd
    # grant execution rights
    sudo chmod ugo+x celeryd
    # now copy the config file for the daemon from the qu4rtet utilities dir
    sudo cp /srv/qu4rtet/utility/celeryd /etc/default/celeryd
    # add the celery user referenced in the config
    sudo adduser celery
    # make sure the system auto-starts and stops
    sudo update-rc.d celeryd defaults
    # start celery and check the status
    sudo /etc/init.d/celeryd start
    sudo /etc/init.d/celeryd status

Next you will paste in the following configuration which is meant to work
with all of the steps you've followed thus far.  If you've deviated from
all of the steps above you may experience errors in your system.

Quickly Test Gunicorn
---------------------
Hop into the qu4rtet directory and see if you can run gunicorn without issue.

.. code-block:: text

    cd /srv/qu4rtet
    sudo gunicorn --bind 0.0.0.0:8000 config.wsgi:application

It should start without error.  Hit CTRL+C to stop the gunicorn server.


Configure Supervisor to Run Gunicorn and Celery Flower
------------------------------------------------------
Here we will daemonize Gunicorn and celery-flower with supervisor (which will also
monitor the process).  The two configuration files in the utility directory
are pre-configured to work with the installation instructions if you followed
them.  Execute the following from the `/srv/qu4rtet` directory:

(If you've decided to use a virtualenv, map /usr/local/bin/celery to your
virtualenv celery.  For example:
*sudo ln -s /home/ubuntu/.virtualenvs/qu4rtet/bin/celery /usr/local/bin/celery*)

.. code-block:: text

    sudo cp ./utility/flower.conf /etc/supervisor/conf.d/flower.conf
    sudo cp ./utility/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

**If you are using a virtual env, you will need to modify your flower.conf
and your gunicorn.con on lines 3.  The command should point to the virtualenv
bins of your gunicorn and flower installs. There are examples in the conf
files to illustrate this.**

Now make sure everything is running:

.. code-block:: text

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status

Configure Nginx
---------------

Create The Log and Media Directories
====================================
If you're not using AWS or another cloud storage system to keep inbound
EPCIS files, etc. then you'll need to tell the system where you want to store
your EPCIS files on the local file system.

First create the log directory:

.. code-block:: text

    sudo mkdir /var/log/quartet
    sudo chown -R www-data:celery /var/log/quartet

Now create the media directory where inbound files will be stored:

    sudo mkdir /var/quartet/media
    sudo chown -R www-data:celery /var/quartet/media


In the utils directory of the qu4rtet directory there is a pre-configured
nginx file.  Copy that file to the nginx directory and then edit it by changing
the `server_name` field from SERVER_DOMAIN_OR_IP to whatever your host name
or server ip address is.  ** Remember to make sure that whatever your
host name is, it is also configured in the .env file under `DJANGO_ALLOWED_HOSTS`
or your static files will not be served by nginx.**

.. code-block:: text

    # copy the config file from the qu4rtet folder
    sudo cp utility/nginx.conf /etc/nginx/sites-available/qu4rtet
    # edit the file by changing the server name to an appropriate server name
    sudo nano /etc/nginx/sites-available/qu4rtet

For example:

.. code-block:: text

    server {
        listen 80;
        # **********************
        # CHANGE THE SERVER NAME
        # **********************
        server_name serial-lab.local;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /srv/qu4rtet;
        }
        location /media/ {
            root /var/qu4rtet/media;
        }
        location / {
            include proxy_params;
            proxy_pass http://unix:/srv/qu4rtet/qu4rtet.sock;
        }
    }
    server{
        listen 5555;
        # **********************
        # CHANGE THE SERVER NAME
        # **********************
        server_name serial-lab.local;

        location / {
            proxy_pass http://127.0.0.1:5544;
            proxy_set_header Host $host;
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            auth_basic "Restricted";
            auth_basic_user_file /etc/nginx/.htpasswd;
        }
    }

Now create a symlink in the sites-enabled directory of nginx and create
the media folder for qu4rtet to store uploaded files with:

.. code-block:: text

    # get rid of the default site if it is there
    sudo rm /etc/nginx/sites-enabled/default
    # add a link to the qu4rtet site
    sudo ln -s /etc/nginx/sites-available/qu4rtet /etc/nginx/sites-enabled
    # make the media folder
    sudo mkdir -p /var/qu4rtet/media
    # give the webserver rights to the media folder
    sudo chown -R www-data:www-data /var/qu4rtet/media/
    # create the error logging folder for qu4rtet
    sudo mkdir -p /var/qu4rtet/logs
    # give nginx rights to the logging folder
    sudo chown -R www-data:www-data /var/qu4rtet/logs
    # test the config
    sudo nginx -t
    # restart the server
    sudo systemctl restart nginx

The last thing to do is create a user for the celery flower administration
page:

.. code-block:: text

    sudo htpasswd -c /etc/nginx/.htpasswd qu4rtet

Modify The HTTPS_ONLY Setting (Optional)
----------------------------------------
If you decide to implement HTTPS on your nginx server, you'll need to change
the HTTPS_ONLY to True in your .env file.

Check the Site
--------------
Your server should be up and running now.  Navigate to it in your browser using
the server name you configured for the web server in the *Nginx* section
of this document.
If you have any questions, reach out to us.  Our contact info, slack-channel
and such is available at http://serial-lab.com

Check the Flower Page
---------------------
The flower page will be exposed on port 5555 of your qu4rtet server.
For example:

`http://myserver.myhost.com:5555`


Optional Sentry and Elastic APM Configurations
-----------------------------------------

Sentry Settings
+++++++++++++++

**NOTE: remember to restart gunicorn if you make any settings changes
recommended in this section.**

If you'd like to use Sentry to monitor your application logs, go to https://sentry.io/
and sign up for a free account, create a `Django` project and follow the
instructions here:

https://sentry.io/serial-lab/my-quartet/getting-started/python-django/

** Change Sentry Settings in .env **

Add your *Sentry DSN* to the following settings in your .env file:

.. code-block:: text

    # set this value to True
    USE_SENTRY=True
    # for example
    DJANGO_SENTRY_DSN=https://fc9e6636bb204f27ad1ef02598d649b3@sentry.example/292104

When you are complete.  Restart the gunicorn server.  This will reload
the settings of your QU4RTET application.

.. code-block:: text

    sudo supervisorctl restart guni:gunicorn


Elastic APM Settings
++++++++++++++++++++
If you'd like to monitor your system performance using Elastic APM, you
can find the software here:

https://www.elastic.co/solutions/apm

After you install your APM server, fill in the following settings in your
`.env` file:

.. code-block:: text

    # set this to True
    USE_ELASTIC_APM=True
    ELASTIC_APM_SERVICE_NAME= # put your service name here
    ELASTIC_APM_SECRET_TOKEN= # put your secret token here
    ELASTIC_APM_SERVER_URL= # if not local host, put the URL/host name here

Restart your QU4RTET services by executing the restart command:

.. code-block::

    restart-quartet

Comments / Issues
-----------------
If you find any errors with this documentation.  Please feel free to create
an issue on our gitlab page at:

https://gitlab.com/serial-lab/qu4rtet/issues


