Expiring Dict
-------------

.. image:: https://travis-ci.org/weaming/expiringdict.svg?branch=master
    :target: https://travis-ci.org/weaming/expiringdict

expiringdict is a Python caching library. The core of the library is ExpiringDict class which
is an ordered dictionary with auto-expiring values for caching purposes. Expiration happens on
any access, object is locked during cleanup from expired values. ExpiringDict can not store
more than `max_len` elements - the oldest will be deleted.

**Note:** Iteration over dict and also keys() do not remove expired values!

Features after fork
-------------------

* optioinal default value passed by dict after keys expired

Installation
------------

If you wish to install from PyPi:

.. code-block:: bash

    pip install expiringdict-with-default

If you wish to download the source and install from GitHub:

.. code-block:: bash

    git clone git@github.com:weaming/expiringdict.git
    python setup.py install


To run tests with coverage:

.. code-block:: bash

    nosetests --with-coverage --cover-package=expiringdict

Usage
-----

Create a dictionary with capacity for 100 elements and elements expiring in 10 seconds:

.. code-block:: py

    from expiringdict import ExpiringDict
    cache = ExpiringDict(max_len=100, max_age_seconds=10, default={'name': 'Alice'})

put and get a value there:

.. code-block:: py

     cache["key"] = "value"
     cache.get("key")
