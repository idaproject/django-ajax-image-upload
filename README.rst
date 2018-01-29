=============================
Django User Assets
=============================

.. image:: https://badge.fury.io/py/django-ajax-image-upload.svg
    :target: https://badge.fury.io/py/django-ajax-image-upload

.. image:: https://travis-ci.org/idaproject/django-ajax-image-upload.svg?branch=master
    :target: https://travis-ci.org/idaproject/django-ajax-image-upload

.. image:: https://codecov.io/gh/idaproject/django-ajax-image-upload/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/idaproject/django-ajax-image-upload

Upload images via ajax.

Documentation
-------------

The full documentation is at https://django-ajax-image-upload.readthedocs.io.

Quickstart
----------

Install Django User Assets::

    pip install django-ajax-image-upload

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'ajaximage',
        ...
    )

Add Django User Assets's URL patterns:

.. code-block:: python

    from ajaximage import urls as ajaximage_urls


    urlpatterns = [
        ...
        url(r'^', include(ajaximage_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
