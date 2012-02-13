=================
Dealing with tags
=================

There are two ways of using zenfroms app.

First way - use ``{% zenform %}`` and ``{% endzenform %}`` template tags.
In the middle of them you can do whatever you want, tags defines a special
conetxt and track form fields usage.

Second way is the use ``{% izenform %}`` tempalte tag. This tag renders all form,
and don't allow you to make modifications in field flow.


{% zenform %} and {% endzenform %}
----------------------------------

**Usage** ::

        {% zenform form [options key1=value1, key2=value2] %}
            Your form goes here!
            {% fieldset unused_fields title 'All my form' %}
        {% endzenform %}

* ``form`` - Django's form
* ``key1=value1, key2=value2`` - options string, which will be converted to a dict.
  you can add your options and use them later in templates

To use this tag pair, you should use ``{% fieldset %}`` tags.
Follow documentation about this tag usage.

**Context**

Tag creates special inner conetxt.

    * ``form`` - original form, passed in arguments
    * ``unused_fields`` - fields, that were not rendered within the tag.
    * ``options`` - options dict specified in tag definition

    Tag can watch what fields were used only when you are rendering them with
    'zenforms' tags. I.e. it couldn't track used and unused fields if you
    place them manually.


**Example**

Render Django's default ``UserCreationForm``::

    {% zenform form %}
        {% fieldset 'username' title 'User data' %}
        {% fieldset unused_fields title 'The rest' %}
    {% endzenform %}


**Templates**

Tags ``{% zenform %}`` and ``{% endzenform %}`` uses two templates to wrap the rendered form:

* ``zenforms/zenform_prefix.html``
* ``zenforms/zenform_postfix.html``

You are welcome to ovreride them in your project.

.. note::

    Zenforms will add a bit of css classes to your widgets. I hope, it wil not crash your app.
    It adds ``textInput`` css class for ``forms.CharField`` and ``forms.EmailField``,
    and ``error`` class for bound fields with errors.


{% fieldset %}
--------------

Second part of ``{% zenform %}``-``{% endzenform %}`` tags is ``{% fieldset %}`` tag.

**Usage:** ::

    {% fieldset 'field1' 'field2' [title 'MyFieldset'] %}
    {% fieldset unused_fields %}

* ``'field1' 'field2'`` - strings with field names, which will be included in fieldset
* ``MyFieldset`` - optionally  you can set fieldsset's title. Therefore, it will be rendered as <h3> tag.

.. warning::

    Aware of use iterable arguments in the ``{% fieldset %}`` tag. Because of ``unused_fields`` argument support,
    this tag consider all iterables as ``unused_fields``.


**Template**

This tag uses ``'zenforms/fieldset.html'`` template. There is nothing interesting there,
only includes and cycles. You wouldn't like to override it.

But in ``zenforms/fields`` you may find something interesting.
Common fields are rendered with ``zenforms/fields/single.html`` template.


{% multifield %}
----------------

If you want to group several fields in one line of form this tag is for you.

**Usage:** ::

    {% multifield args as varname [label 'Label'] %}

* args - List of form field names, which you want to group. Quotes are nessecary,
* varname - output variable name. Quotes are not nessecary,
* label - optional group's name.


Multifield tag returns object recognizable by ``{% fieldset %}`` so you do the following::

    {% multifield 'first_name' 'last_name' as credentials label 'Enter your name' %}
    {% fieldset credentials 'password1' 'password2' %}

**Template**

``{% multifield %}`` tag renders it's contents via ``zenforms/fields/multi.html`` template.
You may override it.

{% readonly %}
--------------

I faced with the task to display data and then edit it. I created this tag as a solution.
``{% readonly %}`` tag renders django's model instance data like it would be in form.

**Usage:** ::

    {% readonly instance 'field1' 'field2' [label 'MyLabel'] [as varname] %}

* ``instance`` - Django model instance
* ``'field1' 'field2'`` - list of instance fields. It is important that model must have that fields
* ``MyLabel`` - you can optionally specify a label for all fields, for example, User data
* ``varname`` - optionally saves rendered fields into template variable for futher usage.

ReadonlyTag also returns recognizable by ``{% fieldset %}`` value, you can mix fields, multifields
and read-olny-fields as you wish. ::

    {% zenform form %}
    {% readonly admin 'username' 'last_name' label 'Your admin data' as admin_data %}
    {% multifield 'first_name' 'last_name' as credentials label 'Enter your name' %}
    {% fieldset admin_data credentials unused_fields %}
    {% endzenform %}

**Template**

``{% readonly %}`` tag renders it's contents via ``zenforms/fields/readonly.html`` template.
You may override it too.


{% submit %}
-------------

Very simple tag. Renders submit button in button holder for you.

**Usage:** ::

    {% submit [value] %}

* ``value`` - submit value, for example, 'Save' or 'Send'


**Template**

Tag uses ``zenforms/submit.html`` tempalte. Override it if you wish.


{% izenform %}
---------------

Finally! The last tag ``{% izenform %}`` renders for without bunch of template tags,
if simply renders all form fields into one fieldset. In the most cases it is tag-what-you-need.

**Usage:** ::

    {% izenform form [options key1=value1, key2=value2] %}

Options are the same as for {% zenform %} tags:

* ``form`` - Django's form
* ``key1=value1, key2=value2`` - options string, which will be converted to a dict.
  you can add your options and use them later in templates

**Template**

Tag uses ``zenforms/zenform_inline.html`` template. Nothing interesting there.
