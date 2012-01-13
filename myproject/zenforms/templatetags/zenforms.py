# -*- coding: utf-8 -*-
from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiValueArgument
from django import template
from django.db.models.fields import FieldDoesNotExist
from django.template import loader
from django.utils.safestring import SafeUnicode


register = template.Library()

class TemplateError(Exception):
    pass


class MultiField(object):
    multifield = True  # For easier template composing

    def __init__(self, form, fields, label):
        self.form = form
        self.field_names = fields
        self.label = label
        self.fields = []
        for field_name in self.field_names:
            try:
                self.fields.append(self.form[field_name])
            except KeyError:
                raise TemplateError('form does not contain field %s' % field_name)

class ReadonlyField(object):
    readonly = True  # For easier template composing

    def __init__(self, label, help_text, meta=None, value=None, fields=None):
        self.label = label
        self.help_text = help_text
        self.meta = meta
        self.value = value
        self.fields = fields

class ZenformTag(Tag):
    """
    Zenform tag is main application tag, it starts with ``{% zenform %}`` and ends with ``{% endzenform %}``

    **Usage** ::

        {% zenform form options %}
            Your form goes here!
            {% fielset unused_fields title 'All my form' %} <- for example
        {% endzenform %}

    **Context**

    * ``form`` - original form, passed in arguments
    * ``unused_fields`` - fields, that were not rendered within the tag.

      Tag can watch what fields are unused only when you are rendering them with
      'zenforms'* tags. I.e. it couldn't track used and unused fields if you
      place them manually.


    **Templates**

    Tags ``{% zenform %}`` and ``{% endzenform %}`` use two templates to wrap the rendered form:

    * ``zenforms/zenform_prefix.html``
    * ``zenforms/zenform_postfix.html``

    You are welcome to ovreride them in your project.

    **Example**

    Render Django's default ``UserCreationForm``::

        {% zenform form %}
            {% fieldset 'username' title 'User data' %}
            {% fieldset unused_fields title 'The rest' %}
        {% endzenform %}
    """
    name = 'zenform'
    options = Options(
        Argument('form'),
        blocks=[('endzenform', 'nodelist')],
    )

    def render_tag(self, context, form, nodelist):
        context.push()
        context['form'] = form
        context['unused_fields'] = form.fields.keys()
        output = self.render_prefix(context) + nodelist.render(context) + self.render_postfix(context)
        context.pop()
        return output

    def render_prefix(self, context):
        template = loader.get_template('zenforms/zenform_prefix.html')
        return template.render(context)

    def render_postfix(self, context):
        template = loader.get_template('zenforms/zenform_postfix.html')
        return template.render(context)


class MultifieldTag(Tag):
    name = 'multifield'
    options = Options(
        MultiValueArgument('fields'),
        'as',
        Argument('varname', resolve=False),
        'label',
        Argument('label', required=False),
    )

    def create_multifield(self, context, fields, label):
        try:
            form = context['form']
        except KeyError:
            raise TemplateError('fieldset tag must be used in {% zenform %}{% endzenform %} context')
        multifield = MultiField(form, fields, label)
        return multifield

    def render_tag(self, context, fields, varname, label):
        mf = self.create_multifield(context, fields, label)
        print mf
        context[varname] = mf
        return u''


class FieldsetTag(Tag):
    name = 'fieldset'
    options = Options(
        MultiValueArgument('fields'),
        'title',
        Argument('title', required=False),
    )
    template = 'zenforms/fieldset.html'

    def udpate_context(self, fields, form, tag_context, unused_fields):
        if type(fields) is list and fields[0] == unused_fields:
            # ``unused_fields`` is the argument
            iterable = tuple(unused_fields)
        else:
            iterable = fields
        for field in iterable:
            try:
                if type(field) in [SafeUnicode, str]:
                    tag_context['fields'].append(form[field])
                    unused_fields.remove(field)
                elif type(field) is MultiField:
                    tag_context['fields'].append(field)
                    for fname in field.field_names:
                        unused_fields.remove(fname)
                elif type(field) is ReadonlyField:
                    tag_context['fields'].append(field)
            except KeyError:
                raise TemplateError('form does not contain field %s' % field)

    def get_context(self, context, title, fields):
        tag_context = {'fields': [], 'title': title}
        try:
            form = context['form']
            unused_fields = context['unused_fields']
        except KeyError:
            raise TemplateError('fieldset tag must be used in {% zenform %}{% endzenform %} context')
        self.udpate_context(fields, form, tag_context, unused_fields)
        context.update(tag_context)
        return context

    def render_tag(self, context, title, fields):
        context = self.get_context(context, title, fields)
        template = loader.get_template(self.template)
        output = template.render(context)
        return output


class Submit(Tag):
    name = 'submit'
    template = 'zenforms/submit.html'
    options = Options(
        Argument('value', required=False, default='Submit'),
    )

    def render_tag(self, context, value):
        context.push()
        context['value'] = value
        template = loader.get_template(self.template)
        output = template.render(context)
        context.pop()
        return output


class ReadonlyTag(Tag):
    name = 'readonly'
    template = 'zenforms/readonly.html'
    options = Options(
        Argument('instance'),
        MultiValueArgument('fields'),
        'label',
        Argument('label', required=False, default=None),
        'as',
        Argument('varname', resolve=False, required=False, default=None),
    )

    def get_context(self, instance, field_names, label):
        opts = instance._meta
        context = {}
        fields = []
        for fname in field_names:
            try:
                f = opts.get_field_by_name(fname)[0]
            except FieldDoesNotExist:
                raise TemplateError('Field %s not exists in a model' % fname)
            else:
                fields.append({'value': f.value_from_object(instance), 'meta': f})

        context['fields'] = fields
        if label:
            context['label'] = label
        else:
            context['label'] = fields[0]['meta'].verbose_name

        context['help_text'] = fields[0]['meta'].help_text
        return context

    def render_tag(self, context, instance, fields, label, varname):
        ctx = self.get_context(instance, fields, label)
        if varname:
            context[varname] = ReadonlyField(**ctx)
            return u''
        else:
            context.push()
            context.update({'readonly': ctx})
            template = loader.get_template(self.template)
            output = template.render(context)
            context.pop()
            return output


register.tag(ZenformTag)
register.tag(MultifieldTag)
register.tag(FieldsetTag)
register.tag(Submit)
register.tag(ReadonlyTag)
