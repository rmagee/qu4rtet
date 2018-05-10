Setting Up Development Environment
==================================
** Note: Make sure you have python3 installed on your system.  QU4RTET was
written in the Python programming language.**

Install instructions for python3 can be found here:

https://www.python.org/

Docker (Optional)
-----------------
The first thing to do is get docker installed, while docker is not necessary
for a development environmnet, it will save you time
as just a simple way to get your `RabbitMQ` and `PostgreSQL` instances up and running. The
QU4RTET celery configuration for local development requires an AMQP (RabbitMQ)
server running locally.  

The latest RabbitMQ docker can be found here:

https://hub.docker.com/_/rabbitmq/

The latest PostgreSQL docker can be found here:

To install and run

.. code-block:: text

    docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:management

This exposes the RabbitMQ management web interface on port 15672 if you want
to access.  http://localhost:15672

For more on that see the RabbitMQ docs.

https://hub.docker.com/_/postgres/

To install

.. code-block:: text

    docker run -d -p 5432:5432 postgres:latest

Other Options
+++++++++++++
If you do not want to use docker, feel free to install per the recommended
methods on the RabbitMQ and Postgres sites for your operating system.

For more:

https://www.rabbitmq.com/

https://www.postgresql.org/

Create Database and Role
------------------------
Create a database and a role in your local database (whether docker or 
native).  For tools and clients to connect to your database and to do this
see the postresql site here:

https://www.postgresql.org/

Or you can download the pgAdmin tool here:

https://www.postgresql.org/

For simplicity's sake, create a database named `qu4rtet` and a user/role
of the same name to manage your system with: *(Do not use these settings in
production.)*

.. code-block::sql

    ﻿CREATE USER qu4rtet WITH
          LOGIN
          SUPERUSER
          INHERIT
          CREATEDB
          CREATEROLE
          REPLICATION;

    CREATE DATABASE qu4rtet
        WITH 
        OWNER = qu4rtet
        ENCODING = 'UTF8'
        LC_COLLATE = 'en_US.UTF-8'
        LC_CTYPE = 'en_US.UTF-8'
        TABLESPACE = pg_default
        CONNECTION LIMIT = -1;

** NOTE: you will need to supply the user name and password in your .env
file in the later steps of this document.**

Download the Code
-----------------

Fork the QU4RTET project and download the code.  (Forking is optional but 
the best option if you plan on developing.)

Fork here
+++++++++

    https://gitlab.com/serial-lab/qu4rtet

Clone locally
+++++++++++++

.. code-block:: text

    git clone git@gitlab.com:[your repo]/qu4rtet.git
    
Create a Local ENV File
+++++++++++++++++++++++
Copy the example .env file from the local utilities folder.

.. code-block:: text

    # file MUST be in the quartet root and named .env
    cp ./utility/env-example.txt .env

In the .env file, change the following to reflect what you set up during the 
database installation:

# Set the POSTGRES_DB to the name of your database.
# Set the POSTGRES_USER to the name of your database user.
# Set the POSTGRES_PORT if you changed the default postgres port for any reason
# Set the POSTGRES_PASSWORD to the password you created for your database user.

For example:

.. code-block:: text
    
    # example config
    POSTGRES_DB=qu4rtet
    POSTGRES_USER=qu4rtet
    POSTGRES_PORT=5432
    POSTGRES_PASSWORD=onetwothreefour4321

Install VirtualEnv
------------------
From the qu4rtet root directory:

For 'Nix and OSX:
*****************

.. code-block:: text
    
    # install virtual env & tools
    pip install virtualenv virtualenvwrapper

Add the following to the tail of your `.bashrc` (linux) or `.bash_profile` (osx)

.. code-block:: text
    
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh

For windows setup:
******************

http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/
https://virtualenv.pypa.io/en/stable/userguide/
https://pypi.org/project/virtualenvwrapper-win/

** Please do not contact serial-lab with windows issues.**

Install Dev Requirements
************************

.. code-block:: text

    # make sure you are using python 3
    mkvirtualenv qu4rtet -p python3
    pip install -r ./requirements/local.txt


Launch Celery and Flower
------------------------
Launch the celery distributed task manager along with *Flower*.  Flower
will allow you to monitor Celery via your web browser at:

http://localhost:5555

To launch:

.. code-block:: text

    celery flower -A qu4rtet.taskapp.celery worker --loglevel=debug --port=5555

Run Database Migrations
-----------------------
The QU4RTET API was written primarily using Django and the 
Django Rest Framework.  For more on Django see:

https://www.djangoproject.com/
http://www.django-rest-framework.org/

Run the database migrations and create a Django superuser.

.. code-block:: text

    # make sure the virtualenv is activated
    workon qu4rtet 

    python manage.py migrate --run-syncdb
    python manage.py makemigrations
    python manage.py migrate   
    python manage.py createsuperuser

Launch the Dev Server
---------------------
Now in your root folder, you can launch the python django development server:

.. code-block:: text

    python manage.py runserver

You should be able to navigate to http://localhost:8000 and see the 
QU4RTET API server running.

Next Steps
----------
From here you can begin any development work using your favorite IDE, etc.

To learn more about the core functionality of QU4RTET see the following:

https://gitlab.com/users/serial-lab/projects

Here you will find core info on the following:

quartet_epcis
    The `quartet_epcis` python package defines the database models, APIs and 
    parsing step for EPCIS XML files. It also defines models for storing
    *GS1 Standard Business Document Header* (SBDH) data as well.

quartet_capture
    The `quartet_capture` package defines the database models, APIs and rule
    engine framework for QU4RTET.

EPCPyYes
    The `EPCPyYes` package allows for the fast and easy development of 
    EPCIS enabled applications by allowing developers to work with EPCIS data
    using simple python classes.

EParseCIS
    The `EParseCIS` package defines the fast XML parser that is the base 
    class for parsing EPCIS data.  The `quartet_epcis` package uses this to
    convert EPCIS data into objects that are saved to the database.

serialbox
    `serialbox` defines the database models, APIs and backed infrastructure
    for generating and allocating serial number ranges.

random_flavorpack
    The `random_flavorpack` is a plugin for SerialBox that exposes API endpoints
    for the generation of randomized numbers.




