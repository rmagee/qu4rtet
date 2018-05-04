Ubuntu/Debian Installation
==========================

Install Requirements
--------------------

.. code-block::text

    sudo apt-get -y install update
    sudo apt-get -y install rabbitmq-server python3-pip postgresql postgresql-contrib gunicorn nginx
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

Paste the following configuration into the .env file and modify accordingly:

.. code-block::text

    POSTGRES_DB=qu4rtet
    POSTGRES_USER=qu4rtet
    DATABASE_HOST=localhost # change this if necessary
    POSTGERS_PORT=5432 # change this if necessary
    #### make sure to put your qu4rtet user's password below !!!! ####
    POSTGRES_PASSWORD=

    CONN_MAX_AGE=60

    # General settings
    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_SECRET_KEY=lLPaGAoJIvUkWltSootWeXDjizxHys2HxUiH24gUoHp1Zw4YwB
    DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1,192.168.1.4'
    DJANGO_DEBUG=False

    # AWS Settings
    DJANGO_AWS_ACCESS_KEY_ID=
    DJANGO_AWS_SECRET_ACCESS_KEY=
    DJANGO_AWS_STORAGE_BUCKET_NAME=

    # Used with email
    DJANGO_MAILGUN_API_KEY=
    DJANGO_SERVER_EMAIL=
    MAILGUN_SENDER_DOMAIN=

    # Security! Better to use DNS for this task, but you can use redirect
    DJANGO_SECURE_SSL_REDIRECT=False

    # django-allauth
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=False
    # Sentry
    DJANGO_SENTRY_DSN=https://fc9e6636aa204f27ad1ef02598d649b3@sentry.io/290104

    DJANGO_OPBEAT_ORGANIZATION_ID='50813ddae7cc4965b2b0cf36e04509ea'
    DJANGO_OPBEAT_APP_ID='727f44d4c1'
    DJANGO_OPBEAT_SECRET_TOKEN='c4ed6c589e9b1b8f72b265cb5a9a1a1fa5ecc4c0'

    CELERY_BROKER_URL="amqp://guest@localhost//"

    USE_AWS=False


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

Set Environment Variables
--------------------------------
Here we will add system wide environment variables that handle the
Django secret key for qu4rtet encryption.

Step 1.  Go here and create a secret key:
https://www.miniwebtool.com/django-secret-key-generator/

Step 2.  Add the secret key to the .env file.  ** Do not use the
example key below!!!** Use the secret key you created in step 1.

.. code-block::text

    sudo nano .env

    # paste your key into the file under the DJANGO_SECRET_KEY setting:
    DJANGO_SECRET_KEY=tzrbhxx=6akus)ttq3e!375lzw43n006gbt^n+w2#si5p0-k5#

**Log out of the system and then log back in for the environment variables
to take effect.**  To make sure the variables are there execute the following:

.. code-block::text

    printenv

You should see your variables in the output list.


Install Gunicorn
------------------

Next we will install Gunicorn which will serve up the qu4rtet application
code via WSGI.

.. code-block::text

    sudo apt-get install -y gunicorn

Make sure it works.  In the root of the qu4rtet download, execute the following:

.. code-block::text

    sudo gunicorn --bind 0.0.0.0:8000 config.wsgi:application

It should start without error.  Hit CTRL+C to stop the gunicorn server.


