Contents:
=========

.. toctree::
   :maxdepth: 2

   usage
   changelog

.. include:: ../README.rst

Installation
============

Istall package::

    pip install django-zenforms

Install ``'zenforms'`` in ``INSTALLED_APPS``.

And put static files on page::

    <link rel="stylesheet" href="{{ STATIC_URL }}zenforms/css/uni-form.css" type="text/css" />
    <link rel="stylesheet" href="{{ STATIC_URL }}zenforms/css/default.uni-form.css" type="text/css" />

    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}zenforms/js/uni-form.jquery.min.js"></script>


