SFTP Directory Monitoring
=========================

Configure chrooted SFTP Directory
---------------------------------

Follow the instructions for your given operating system or, if using, Ubuntu/Debian,
here is a nice example tutorial: `Setup chrooted SFTP`_

.. _Setup chrooted SFTP: https://www.ostechnix.com/setup-chrooted-sftp-linux/


Set up Logging Directories
--------------------------

Create an output and error log location directory for your directory
monitoring process.  We recommend the following

.. code-block:: text

    sudo mkdir /var/log/quartet/

Supervisor Configuration
------------------------

Install *supervisor* if it is not already installed.

Create a configuration in the /etc/supervisord/conf.d directory with
the following values.  Set execution rights to this file for all, user &
group using `chmod`.  NOTE: **replace the username directory to monitor below where it
says "[replace with username]".  Also, if you are not using a virtual env
or have not used the suggested quartet directory naming conventions, change
the values below accordingly.

.. code-block:: text
[program:folder_monitor]
directory=/srv/qu4rtet
command=sudo /home/qu4rtet/.virtualenvs/qu4rtet/bin/python /srv/qu4rtet/manage.py watch_inbound_folders "/sftp/[replace with username]/" "/var/quartet/processed_sftp/" "sftponly"
autostart=true
autorestart=true
stderr_logfile=/var/log/quartet/folder_monitor.err
stdout_logfile=/var/log/quartet/folder_monitor.out
user=root
group=qu4rtet
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8


[group:foldermon]
programs:folder_monitor

Load Supervisor Config
----------------------

After you add your new supervisor folder monitor service config file, you
need to tell supervisor to load it:

.. code-block:: text

    sudo supervisorctl update

To see if it is running:

.. code-block:: text

    sudo supervisorctl status

About the `watch_inbound_folders` management command
----------------------------------------------------

This is django management command that is part of the `quartet_capture`
python package.  Configuring it to run as a daemon is documented here since
this is a default package with QU4RTET and the daemonization of the management
command is specific to server / platform roll-outs.

You provide three parameters to the command.  The first is the directory to
monitor.  The second is the directory to place files that have been processed.
Think of this as an archive directory.  The last is the group name to associate
any processed files with as they are place in the archive directory.

Directories Will Be Created for Each Rule
=========================================

For every rule you have defined in q4, you will find that the *watch_inbound_folders*
command will create a folder with the same name.  When users drop files
into a folder with a specific name, the monitor will grab that file and
pass it to the rule corresponding with the file name.


