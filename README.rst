Django-Db-Snapshot
==================

What's that
-----------
Reusable Django app for fully automatic database snapshots.
We are using it for backup big databases (100GB+).
App can be run on several instances and managing from one place.


Installation
------------

1. Install backup server with LVM support. Install and configure ``mylvmbackup`` config file

.. code-block:: bash

    $ apt-get install mylvmbackup
    $ cp /etc/mylvmbackup.conf{,.bak}
    $ cat > /etc/mylvmbackup.conf << END
    [mysql]
    user=root
    password=123password123

    socket=/var/run/mysqld/mysqld.sock

    [lvm]
    vgname=vg0
    lvname=mysql
    lvsize=2G
    END

2. Install ``dbsnapshot`` using pip:

.. code-block:: bash

    $ pip install django-db-snapshot

3. Add the ``dbsnapshot`` application to ``INSTALLED_APPS``
4. Configure django-celery on project settings

.. code-block:: bash

    $ apt-get install redis-server
    $ pip install django-celery

.. code-block:: python

    INSTALLED_APPS += ('djcelery',)

    BROKER_URL = 'redis://127.0.0.1:6379/1'
    CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

    import djcelery
    djcelery.setup_loader()


5. Sync database (``./manage.py syncdb`` or ``./manage.py migrate``)
6. Run internal dbsnapshot server (``./manage.py run_dbsnapshot_server``)
7. Restart Redis instance

.. code-block:: bash

    $ /etc/init.d/redis-server restart

8. Add backup server and configure backup options on django admin interface (``/admin/dbsnapshot/server/``)
9. That's all. Enjoy.


Demo
----

.. code-block:: bash

    $ apt-get install virtualenvwrapper redis-server
    $ mkvirtualenv django-db-snapshot
    $ git clone https://github.com/LPgenerator/django-db-snapshot
    $ cd django-db-snapshot
    $ python setup.py develop
    $ cd demo
    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py migrate
    $ redis-server >& /dev/null &
    $ python manage.py runserver >& /dev/null &
    $ xdg-open http://127.0.0.1:8000/admin/


Backup server configuration
---------------------------

.. code-block:: bash

    $ sudo -i
    $ cd /srv/
    $ apt-get install python-mysqldb python-django python-pip supervisor
    $ pip install django-db-snapshot
    $ django-admin startproject dbback
    $ cd dbback/
    $ cat >> dbback/settings.py << END
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mysql',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3306,
            'TEST_COLLATION': 'utf8_general_ci',
        }
    }
    INSTALLED_APPS += ('dbsnapshot',)
    DBS_SERVER_HOST = '0.0.0.0'
    DBS_SERVER_PORT = 61216
    END
    $ tail -12 dbback/settings.py
    $ iptables -A INPUT -p tcp --dport 61216 -j ACCEPT
    $ python manage.py run_dbsnapshot_server
    $ cat > /etc/supervisor/conf.d/dbsnapshot.conf << END
    [program:dbsnapshot_server]
    command=/usr/bin/python /srv/dbback/manage.py run_dbsnapshot_server
    user=root
    numprocs=1
    autostart=true
    autorestart=true
    stdout_logfile=/var/log/dbsnapshot.log
    stderr_logfile=/var/log/dbsnapshot.err.log
    startretries=25
    END
    $ /etc/init.d/supervisor restart
    $ supervisorctl status


Screenshots
-----------
.. image:: /screenshots/server_change_list.jpg
.. image:: /screenshots/logs_chage_list.jpg


Compatibility:
-------------
* Python: 2.6, 2.7
* Django: 1.4.x, 1.5.x, 1.6.x
