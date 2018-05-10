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

Then navigate your browser to the following:

** QU4RTET **
http://localhost:8000







