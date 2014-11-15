MagicRanker
===========

MagicRanker is an open-source stock marking ranking and filtering tool based on the `Magic Formula <http://www.magicformulainvesting.com/>`_.

You can view it in action at `MagicRanker.com <http://MagicRanker.com>`_.

Getting Started
---------------

1. Clone repo.

::
  
    git clone git@github.com:lextoumbourou/magicranker.com.git

2. Prepare a `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`_.

::

    cd magicranker.com && virtualenv env

3. Install requirements.

::

    pip install -r requirements.txt


Running tests
--------------

::

    > python manage.py test


To do list
-----------

1. Update scrapers to dump CSV to a Git repo (and make it publically available).
2. Create PG import scripts.
3. Move scrapers out of repo.
4. Flake8 repo.
5. Make use of simple-ranker.
