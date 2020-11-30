File Size and Timeout Settings
==============================

Upload File Size Adjustments
----------------------------

If you find you are getting errors while uploading large files to be
processed you are likely to get one of two types of errors: a file size
"Entity too large" error and/or a task will simply time out because
it took too long to complete.

The configuration for file size relative to uploads can be adjusted at
the bottom of the config file below

.. code-block:: text

    /config/settings/production.py

.. code-block:: python

    DATA_UPLOAD_MAX_MEMORY_SIZE=6553600 #this would be 65 megabytes for example
    FILE_UPLOAD_MAX_MEMORY_SIZE=6553600


In addition, if you are using Nginx as a web server, you will need to configure
your Nginx settings to allow files of a given size.  See the Nginx
documentation relative to the following setting:

.. code-block:: text

    client_max_body_size

For example, you would want to modify the client_max_body_size value below in
your config file if you were using Nginx:

.. code-block:: text

        server {
        ...
        server_name testing123.qu4rtet.io;
        client_max_body_size 20M;
        location = /favicon.ico { access_log off; log_not_found off; }
        ...
        }



Task Timeout Adjustments
------------------------

QU4RTET relies on the :code:`quartet_capture` python package to handle
the processing of tasks.  quartet_capture utilizes the Celery distributed
task framework to accomplish the distribution of tasks.  There is typically
a hard-timeout and soft-time out configuration in the celeryd daemon
configuration file (if you are following our recommended install).

The following line is the one you want to adjust.  If you are using the
default Celery timeouts then you'll want to add this configuration.

.. code-block:: python

    # Extra command-line arguments to the worker
    CELERYD_OPTS="--time-limit=11000 --soft-time-limit=10800" #three hours


If you have adjusted any or all of these make sure to restart Nginx and
Celery.

