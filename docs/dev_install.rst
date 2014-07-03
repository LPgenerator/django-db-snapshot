Installation for development
============================

.. code-block:: bash

    $ sudo apt-get install virtualenvwrapper
    $ mkvirtualenv django-db-snapshot
    $ git clone https://github.com/LPgenerator/django-db-snapshot.git
    $ cd django-db-snapshot
    $ python setup.py develop
    $ cd demo
    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py migrate
    $ python manage.py shell


.. code-block:: python

    >>> import dbsnapshot
    >>> print dbsnapshot.get_version()
