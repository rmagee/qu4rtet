Using the VirtualBox Image
==========================
**NOTE: The virtualbox images are not part of our build process.  You
are best to update QU4RTET following the instructions below once you launch
the virtualbox image for the first time!**

The virtualbox image is for development and testing use but does contain
a fairly production ready deployment minus any SSL.  It is configured
with the following:

# Ubuntu 18.04
# PostgreSQL Database Backend
# NGINX Reverse Proxy Listening on Port 80
# Gunicorn
# 5 Celery Distributed Task Queue Workers

Connecting with QU4RTET-UI
--------------------------
The quartet UI download links can be found on the gitlab site:

https://gitlab.com/serial-lab/quartet-ui

To connect with QU4RTET-UI:

# Launch the virtual-box image
# Login with the default password and user
    * user: qu4rtet
    * password: onetwothreefour4321
# Get the ip address of your virtualbox image by executing `ifconfig`
# In QU4RTET-UI use the ipaddress as the host name and use the same
username and password to configure.

Using Your Own QU4RTET Code
---------------------------
If you've forked QU4RTET (or any of it's components)
and would like to use that, the code
for QU4RTET is in the `/srv/qu4rtet` directory.  You can modify the
`.git/config` file there to point to your repo.  Calling `quartet-update`
will now pull from your repo but will still install all of the serial-lab
quartet components from PyPi.  If you want to install your own forked
components as well, modify the `/usr/local/bin/quartet-update` file and
set the pip install commands to point to your repos or PyPI packages
accordingly.

Upgrading and Restarting QU4RTET
--------------------------------
If you want to update or restart all of the QU4RTET services on the
virtualbox image, use the commands below from the command line:

* `stop-quartet` stops all QU4RTET services, nginx, gunicorn and celery workers.
* `start-quartet` starts all the quartet services and web servers, celery...
* `update-quartet` will pull the latest tag down from the quartet gitlab repo
and update the system with all of the latest serial-lab components.
* `restart-quartet` restarts all quartet, nginx, celery workers, etc.


