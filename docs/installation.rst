Installation
============

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
