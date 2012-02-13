Django zenforms
===============

I definitely going mad about forms in Django. They keep all layout buisness in python code.

Dragan Babić make a simple yet wonderful form css+jquery framework, called `uniforms <http://sprawsm.com/uni-form/>`_. I liked it a lot. In this app I tried to save all original Dragan's work
and adapt to it.

Since I met great app, `django-crispy-forms <https://github.com/maraujop/django-crispy-forms>`_ (ex. django-uni-forms),
I promised to myself to do something like that but templates. And I did.


Quickstart:
===========

Django way::

    <form action="/contact/" method="post">
        {{ form.non_field_errors }}
        {% for field in form %}
            <div class="fieldWrapper">
                {{ field.errors }}
                {{ field.label }} {{ field }}
                {% if field.help_text %}
                <p class="formHint">{{ field.help_text }}</p>
                {% emdif %}
            </div>
        {% endfor %}
        {% csrf_token %}
    </form>

Zenforms way::

    {% izenform form %}

or::

    <form action="." method="post">
    {% izenform form1 options no_form_tag=1 %}
    {% izenform form2 options no_form_tag=1 %}
    <input type="submit" />
    </form>

Regroup fields? as you wish::

    {% zenform form %}
        {% fieldset 'username' title 'User data' %}
        {% multifield 'phone1' 'phone2' as phones label 'Phones' %}
        {% fieldset 'first_name' 'last_name' phones %}
        {% fieldset unused_fields title 'Rest stuff' %}  <!-- you can foget something, zenforms can take care about it -->
    {% endzenform %}

Moreover, you can include read-only values from Django models::

    {% readonly admin 'username' 'last_name' label 'Information' %}

See full documentation.