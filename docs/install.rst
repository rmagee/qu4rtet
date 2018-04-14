Installation
============
With the *Docker Compose* builds you can be up and running in minutes.
If you wish to do a full manual install on a server or laptop, etc.  Follow
the local installation instructions below.

Docker Compose
==============
The docker compose config for local installs runs the following:

1. A postgresql lates version container.
2. A Django/Ubuntu latest version container exposing port 8000.
3. A mailhog 1.0 container exposing port 8025
4. A RabbitMQ container.
5. A celery worker container.
6. A celery beat container.

Download QU4RTET
----------------
Requires Git.  See https://git-scm.com/ if you don't know what that is...

.. code-block:: text

    git clone git@gitlab.com:serial-lab/qu4rtet.git

Install Docker
--------------
You can get docker here:

https://www.docker.com/community-edition

Run Docker Compose
------------------
Run these two commands:

.. code-block::

    docker-compose -f local.yml build
    docker-compose -f local.yml up

Then navigate your browser to the following:

** QU4RTET **
http://localhost:8000


Manual Installation
===================

Get RabbitMQ
-------------------------
RabbitMQ is used as a task broker for *Celery*- which is what QU4RTET uses
as a distributed task engine. You can get a RabbitMQ docker image on
DockerHub here: https://hub.docker.com/_/rabbitmq/

Run the docker container using:

.. code-block::

    docker run rabbitmq --expose

Or install it using the install instructions here:

https://www.rabbitmq.com/download.html

Make sure to start the RabbitMQ service.  :->

Install Celery
--------------
Installing celery is fairly straight-forward.  You can find the instructions
here.

http://www.celeryproject.org/install/

Install PostgreSQL
------------------
We recommend postgresql but you can really use any backend supported by
the Django project.  We use the Django ORM to maintain the abstraction between
the back-end and the API layer in order to provide users with the widest
choice possible for a backend database.

Binary installers for most platforms can be found here:

https://www.postgresql.org/download/


Download QU4RTET
----------------
Requires Git.  See https://git-scm.com/ if you don't know what that is...
We recommend you use virtualenv and virtualenvwrapper for the QU4RTET
python environment.  Note: **QU4RTET requires python 3 or greater to run.**

.. code-block:: text

    # create the virtualenv
    mkvirtualenv qu4rtet

    # get the code
    git clone git@gitlab.com:serial-lab/qu4rtet.git

    # install the requirements
    cd qu4rtet
    pip install -requirements.txt

Start Celery
------------

From the `qu4rtet` root directory, enter in this command (debug flag is
optional).

.. code-block:: text

    celery -A qu4rtet.taskapp.celery worker --loglevel=debug

Start QU4RTET
-------------
From the root directory of QU4RTET run the following command.  This will launch
the dev server.

.. code-block:: text

    python manage.py runserver

Navigate your browser to http://localhost:8000


