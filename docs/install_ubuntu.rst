Ubuntu/Debian Installation
==========================

Before You Begin
----------------
If you are familiar with python and have good unix skills, you may want to
consider using a virtual environment and adjusting the paths in this document
as necessary where necessary.  The only paths that will change for the install
if you decide to do this would be the celery, gunicorn and flower paths.

ALSO!  It is important to follow all of the recommended paths and commands in this
document.  Not doing so will result in much heartache and wasting of time.  If you
decide to use different locations, naming conventions, etc. any support for issues
you may find in the docs will be promptly ignored.

Make sure to:

    1. Always copy and paste the commands as expressed in the doc.
    2. When an example says "change this setting", etc. make sure to change the setting.


Install The Requirements
------------------------
As you can see below, you will need a flavor of python3 and pip3 which may or may not be present on
your base installation of Debian or Ubuntu.  Installing Python and using the
setup tools is well documented and is beyond the scope of this document.  The pip
installation is included below.


.. code-block:: text

    sudo apt-get -y update
    sudo apt-get -y install rabbitmq-server python3-pip postgresql postgresql-contrib gunicorn nginx supervisor apache2-utils python3-dev
    # IF USING PYPY you will need pypy3-dev
    # sudo apt-get install pypy3-dev
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
    # now IN psql execute tll /he following to change the passwords
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

Make sure to exit the postgres user shell

.. code-block::

    exit

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
    DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
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

Then run the migrate and collectstatic commands

.. code-block:: text

    sudo python3 manage.py migrate
    sudo python3 manage.py collectstatic --no-input

Create a Super User Account
---------------------------

.. code-block:: text

    sudo python3 manage.py createsuperuser

Create all The QU4RTET Directories
----------------------------------
QU4RTET will need to have rights, via celery and the nginx webserver accounts
to write out to the log and number files and to also access media files for images
and EPCIS data, etc.  Execute the following below to
create these files.

.. code-block:: text

    sudo useradd -r celery
    sudo mkdir /var/log
    sudo mkdir /var/log/quartet
    sudo chown -R www-data:celery /var/log/quartet
    sudo chmod og+w /var/log/quartet
    sudo chmod ug+s /var/log/quartet
    sudo mkdir /var/quartet
    sudo mkdir /var/quartet/numbers
    sudo chown -R www-data:celery /var/quartet
    sudo chmod ug+w /var/quartet/numbers
    sudo chmod ug+s /var/quartet/numbers
    sudo mkdir /var/quartet/media
    sudo chown -R www-data:celery /var/quartet/media
    sudo chmod ug+s /var/quartet/media
    sudo mkdir /var/run/celery
    sudo chown celery:celery /var/run/celery

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

Here we are going to folllow the *systemd* recommendations on the
celery website that can be found here: https://docs.celeryproject.org/en/latest/userguide/daemonizing.html#service-file-celery-service

However, since the directories are slightly different for the latest version
of Ubuntu, we will modify some of the scripts to reflect this.

Copy the celery.service File to /etc/systemd/system
+++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: text

    # from the qu4rtet root directory
    sudo cp ./utility/celery.service /etc/systemd/system/celery.service

Copy the celery.conf File to /etc/systemd
+++++++++++++++++++++++++++++++++++++++++

.. code-block:: text

    # from the qu4rtet root directory
    sudo cp ./utility/celery.conf /etc/systemd/celery.conf

Modify the Conf File
++++++++++++++++++++
The celery.conf file has pointers to the CELERY_BIN which assumes a user
name of `ubuntu` and a .virtualenv path.  Modify this to point to your
celery binary file.  To find out where your celery install is, execute

.. code-block:: text

    which celery

In addition, there are other configurations for the celery daemon in the
file that are documented on the celery site.  If you'd like to change the
number of workers, time limits, concurrency, etc...then you will need
to modify this file.

Make Sure Celery Has Rights to Log in /var/log/quartet/
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

If celery does not have rights to log in this directory, the daemon will not
start.  Double check that the celery group is an owner and that it has
write permissions to the files in this directory.  See the section above
about creating the log files and make sure you followed it correctly and
that there were no errors during the creation of these directories and the
subsequent assignment of rights.

Once you have confirmed these rights, load the daemon and run it.

.. code-block:: text

    sudo systemctl daemon-reload
    sudo systemctl start celery.service
    sudo systemctl status celery.service

If the service does not start, this is typically due to rights issues
for the celery log file locations and/or rights to the /var/log/quartet/quartet.log

Quickly Test Gunicorn
---------------------
Hop into the qu4rtet directory and see if you can run gunicorn without issue.

.. code-block:: text

    cd /srv/qu4rtet
    sudo `which gunicorn` --bind 0.0.0.0:8000 config.wsgi:application

It should start without error.  Hit CTRL+C to stop the gunicorn server.

Daemonize Gunicorn and Celery Flower
------------------------------------
As of QU4RTET 3.0, the utility scripts have been updated to use systemd
instead of supervisor.  If you are installing from a fresh install, then
this should be of no concern.  If you are revisiting this document to
figure out or debug an issue, make sure to pull down a version of QU4RTET
that matches your own and view the documentation relative to that version.

All of the paths in the scripts we will use below are assuming that there
is a virtualenv named qu4rtet and that the binaries for this python environment
live in the `/home/ubuntu/.virtualenvs/qu4rtet/bin` directory.  This may
likely not be the case for you.

Copy the Gunicorn Service Files
+++++++++++++++++++++++++++++++

.. code-block:: text
    sudo cp ./utility/flower.service /etc/systemd/system/flower.service
    sudo cp ./utility/gunicorn.service /etc/systemd/system/gunicorn.service
    sudo cp ./utility/gunicorn.socket /etc/systemd/system/gunicorn.socket

Modify the ExecStart Command
++++++++++++++++++++++++++++

Open each of the .service files you copied above and modify the line beginning
with `ExecStart` to reflect the location of your gunicorn and flower
bin files.  If you are using a virtualenv named qu4rtet, you can leave
them alone.

Now load and run the services.

.. code-block:: text

    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn.socket
    sudo systemctl status gunicorn.socket
    sudo systemctl restart gunicorn.service
    sudo systemctl status gunicorn.service
    sudo systemctl restart flower.service
    sudo systemctl status flower.service

If gunicorn does not start make sure your ExecCommand is correct by executing
it manually in the terminal.

Configure Nginx
---------------

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

Now create a symlink in the sites-enabled directory of nginx and create
the media folder for qu4rtet to store uploaded files with:

.. code-block:: text

    # get rid of the default site if it is there
    sudo rm /etc/nginx/sites-enabled/default
    # add a link to the qu4rtet site
    sudo ln -s /etc/nginx/sites-available/qu4rtet /etc/nginx/sites-enabled
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


