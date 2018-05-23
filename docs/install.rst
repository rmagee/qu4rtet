Local Installation With Docker Compose
======================================
With the *Docker Compose* builds you can be up and running in minutes.
If you wish to do a full manual install on a server or laptop, etc.  Follow
the local installation instructions below.

Local Docker Compose
--------------------
The docker compose config for local installs runs the following:

1. A postgresql latest version container.
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

.. code-block:: text

    docker-compose -f local.yml build
    docker-compose -f local.yml up

To bring down the images, use the following command:

.. code-block:: text

    docker-compose -f local.yml down

Then navigate your browser to the following:

** QU4RTET **
http://localhost:8000

Create a Super User
-------------------
If you want to connect to this instance using the QU4RTET-UI application,
connect to the `qu4rtet_django_1` docker container and create a superuser
to authenticate with using the following commands:

.. code-block:: text

    # connect to the quartet django container
    docker exec -i -t qu4rtet_django_1 /bin/bash
    # now create a superuser
    python manage.py createsuperuser

Get QU4RTET-UI and Connect
--------------------------
You can find instructions on dowloading and installing QU4RTET-UI here:

    https://gitlab.com/serial-lab/quartet-ui

Then you can follow the instructions for connecting with QUARTET-UI here:

    https://serial-lab.gitlab.io/quartet-ui/




