Redhat Enterprise Linux Installation
====================================

Install Python 3.7
------------------

Follow the instructions here to install Python 3.7

https://tecadmin.net/install-python-3-7-on-centos/

Next, you'll edit the sudoers file and add the /usr/local/bin to the
secure_path:

.. code-block:: text

    # install vim if it's not there
    sudo yum -y install vim
    # edit the sudoers file
    sudo vim /etc/sudoers

Since the python 3.7 bin will be installed in /usr/local/bin, you will
not be able to pip install anything until you add that to the path.

Create a simlink for pip3.7:

.. code-block:: text

    cd /usr/local/bin
    sudo ln -s pip3.7 ./pip

Install Virutalenv
------------------

.. code-block:: text

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper

Configure virtualenvwrapper by adding the following to your ~/.bash_profile:

.. code-block:: text

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh
    workon qu4rtet

Create the qu4rtet Virtual Environment for Python
-------------------------------------------------

.. code-block:: text

    mkvirtualenv qu4rtet

Get QU4RTET from gitlab
-----------------------

.. code-block:: text

    # go to the srv directory
    cd /srv
    # pull down quartet
    sudo git clone https://gitlab.com/serial-lab/qu4rtet.git
    # install quartet requirements
    cd qu4rtet
    pip install -r requirements/production.txt
    # give yourself rights to the directory
    cd ..
    sudo chown -R ec2-user qu4rtet/

Optional: Install PostgreSQL Locally
------------------------------------

If you'd like to use a local database from scratch, follow the instructions here
to install postgres:

https://www.postgresql.org/download/linux/redhat/

Make sure to search for the proper version of the OS you are running on.

Edit the config file:

.. code-block:: text

    # change to postgres user
    sudo -i -u postgres
    # edit file
    vim /var/lib/pgsql/11/data/pg_hba.conf

You will change the `ident` values in the local, IPv4 and IPv6 entries
at the bottom of the file to `md5`.  This allows us to use the -U and -P
command line options when we create the users and datatabase schema next.

After you are done editing the file, save it.  Exit the shell and restart
the database:

.. code-block:: text

    # exit the postgres user shell
    exit
    # restart the database
    systemctl restart postgresql-11


Create The QU4RTET Database
+++++++++++++++++++++++++++

Next you will create the QU4RTET database along with the QU4RTET database user.

.. code-block:: text

    # change to postgres user
    sudo -i -u postgres
    # create the user and database
    createuser -P -d -l -r -S -i --replication --host=localhost --port=5432 qu4rtet
    createdb -e -E UTF8 -O qu4rtet --host=localhost --port=5432  qu4rtet 'The QU4RTET database backend.'



Create an .env file
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

    workon qu4rtet
    python manage.py migrate
    python manage.py collectstatic --no-input
    python manage.py createsuperuser

Run The Dev Server
------------------

A quick test of the configuration is to run the dev server as below.

.. code-block:: text

    python manage.py runserver

If it runs without error we are good for now- even if it returns a 400 HTTP
status that's Ok.  Kill the test server with a
`CTRL+C` and we will move on.


Create the Media and Log directories
------------------------------------

.. code-block:: text

    sudo mkdir /var/quartet
    sudo mkdir /var/quartet/media
    sudo mkdir /var/log/qu4rtet
    # we will change this to www-data:celery later but here we give
    # the ec2-user rights to the log directory so we can run some tests
    sudo chown -R ec2-user /var/log/quartet


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
    sudo cp /srv/qu4rtet/utility/celeryd-redhat /etc/default/celeryd
    # add the celery user referenced in the config
    sudo adduser celery
    # make sure the system auto-starts and stops
    sudo update-rc.d celeryd defaults
    # start celery and check the status
    sudo /etc/init.d/celeryd start
    sudo /etc/init.d/celeryd status

Quickly Test Gunicorn
---------------------
Hop into the qu4rtet directory and see if you can run gunicorn without issue.

.. code-block:: text

    cd /srv/qu4rtet
    gunicorn --bind 0.0.0.0:8000 config.wsgi:application

It should start without error.  Hit CTRL+C to stop the gunicorn server.

Run Gunicorn as a Service
-------------------------

First create a file by opening it in vim

.. code-block:: text

    sudo vim /etc/systemd/system/gunicorn.service

Next add the following to the file

.. code-block:: text

    [Unit]
    Description=gunicorn daemon
    After=network.target

    [Service]
    User=ec2-user
    Group=ec2-user
    WorkingDirectory=/srv/qu4rtet
    ExecStart=/home/ec2-user/.virtualenvs/qu4rtet/bin/gunicorn --workers 3 --bind unix:/srv/qu4rtet/qu4rtet.sock config.wsgi:application

    [Install]
    WantedBy=multi-user.target

Save the file, run the service and enable it to run on boot.

.. code-block:: text

    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn


Install NGINX
-------------

Use the following to install NGINX.

.. code-block:: text

    cd ~
    wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    sudo rpm -ivh epel-release-latest-7.noarch.rpm
    sudo yum --enablerepo=epel install nginx
    rm epel-release-latest-7.noarch.rpm

Once NGINX is installed, we can configure it to communicate with QU4RTET through
gunicorn.

Edit the nginx.conf file:

.. code-block:: text

    sudo vim /etc/nginx/nginx.conf

Within the configuration file, delete the existing server section and add
the following:

.. code-block:: text

    server {
        listen 80;
        # **********************
        # CHANGE THE SERVER NAME
        # **********************
        #server_name myserver.quartet.local;
        client_max_body_size 10M;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static {
            alias /srv/qu4rtet/staticfiles;
        }
        location /media/ {
            root /tmp;
        }
        location / {
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Protocol $scheme;
            proxy_pass http://unix:/srv/qu4rtet/qu4rtet.sock;
        }
    }

Obviously, as the comment section in the text above would suggest, you
will need to configure the host name of your system by uncommenting the
`server_name` line and putting in the appropriate host name or ip address.

SELinux Config
--------------

If you are getting `Bad Gateway` issues it is most likely due to SELinux
being activated and blocking traffic between NGINX and the Gunicorn socket.

.. code-block:: text

    #this should fix the issue
    sudo yum install policycoreutils-python
    sudo semanage permissive -a httpd_t

Add Host to ALLOWED_HOSTS
-------------------------

Make sure to add your host name to ALLOWED_HOSTS in the .env file in your
root directory once you have your DNS configured.  If you are not using DNS
then use the public ip address of the server to do this.

