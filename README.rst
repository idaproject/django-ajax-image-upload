=============================
Django Ajax Image Upload
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

Install Django Ajax Image Upload::

    pip install django-ajax-image-upload

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'adminsortable',
        'ajaximage',
        ...
    )

Add Django Ajax Image Upload's URL patterns:

.. code-block:: python

    from ajaximage import urls as ajaximage_urls


    urlpatterns = [
        ...
        url(r'^', include(ajaximage_urls)),
        ...
    ]

Define your Image model:
.. code-block:: python

    from ajaximage.models import AbstractImage


    class MyImage(AbstractImage):
        # define additional fields here

        class Meta:
            ...


Define generic tabular inline
.. code-block::python

    from ajaximage.admin import ImageInline

    from .models import MyImage


    class MyImageInline(ImageInline):
        models = MyImage

Example usage of AjaxImageUploadMixin:
.. code-block::python

    models.py


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
