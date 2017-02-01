MagicRanker
===========

MagicRanker is an open-source stock marking ranking and filtering tool based on the `Magic Formula <http://www.magicformulainvesting.com/>`_.

You can view it in action at `MagicRanker.com <http://MagicRanker.com>`_.

Dependancies
------------

Postgres (> 9.3)
^^^^^^^^^^^^^^^^

Ubuntu 14
``````````

Postgres can be installed on Ubuntu 14 as follows:

::

     sudo apt-get install postgresql-9.3

OSX
````

I recommend using `Postgres.app <http://postgresapp.com/>`_: "Just download, drag to the applications folder, and double-click"

Windows
```````

Dunno. LOL. Pull request me up if you figure it out.


Node tools
^^^^^^^^^^

Less is required for compiling CSS and Bower for installing static files.

::

    npm install -g bower less


Getting Started
---------------

* Create database and user.

::

    > createuser -W magicranker
    Password:
    > createdb magicranker

* **Coming soon** Download nightly data dump and load into DB.

* Clone repo.

::
  
    git clone git@github.com:lextoumbourou/magicranker.com.git

* Prepare a `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`_.

::

    cd magicranker.com && virtualenv env

* Install Python requirements.

::

    pip install -r requirements.txt

* Install Bower deps.

::

    python manage.py bower install

* Run webserver.

::

     python manage.py runserver

Running tests
-------------

::

    > python manage.py test

Installation with Docker
------------------------

**Note: still working on this section.**

MagicRanker can  be configured with Docker, as follows:

```
docker-compose build
docker-compose up -d
docker-compose run web python /code/manage.py migrate stock
docker-compose run web python /code/manage.py bower install
docker-compose run web python /code/manage.py collectstatic --noinput
docker-compose run web python /code/manage.py compress
```





To do list
-----------

1. Update scrapers to dump CSV to a Git repo (and make it publically available).
2. Create PG import scripts.
3. Move scrapers out of repo.
4. Flake8 repo.
5. Make use of simple-ranker.
