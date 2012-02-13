# -*- coding: utf-8 -*-
from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiValueArgument, MultiKeywordArgument
from django import template
from django.db.models.fields import FieldDoesNotExist
from django.forms.forms import BoundField
from django.template import loader
from django.utils.safestring import SafeUnicode
from django import forms


DEFAULT_OPTIONS = {
    'method': 'post',
    'action': '.',
}
register = template.Library()

class TemplateError(Exception):
    pass


class MultiField(object):
    """
    Inner object for ``MultifieldTag`` class rendering. You probably don't need to know about this class
    """
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
    """
    Inner object used for object representing in ``ReadonlyTag``.
    You probably don't need to know about this class too.
    """
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

    **Usage**::

        {% zenform form [options key1=value1, key2=value2] %}
            Your form goes here!
            {% fieldset unused_fields title 'All my form' %}
        {% endzenform %}

    """
    name = 'zenform'
    options = Options(
        Argument('form'),
        'options',
        MultiKeywordArgument('options', required=False, default=DEFAULT_OPTIONS),
        blocks=[('endzenform', 'nodelist')],
    )
    field_mapping = {
        forms.CharField: 'textInput',
        forms.EmailField: 'textInput',
    }

    def prepare_form(self, form):
        for field in form:
            css_class = ''
            try:
                css_class = self.field_mapping[type(field.field)]
            except KeyError:
                pass
            if field.name in form.errors:
                css_class += ' error'

            if 'class' in field.field.widget.attrs:
                field.field.widget.attrs['class'] += ' %s' % css_class
            else:
                field.field.widget.attrs['class'] = ' %s' % css_class
        return form

    def render_tag(self, context, form, options, nodelist):
        context.push()
        real_options = DEFAULT_OPTIONS.copy()
        real_options.update(options)
        context['form'] = self.prepare_form(form)
        context['options'] = real_options
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


class InlineZenformTag(ZenformTag):
    name = 'izenform'
    options = Options(
        Argument('form'),
        'options',
        MultiKeywordArgument('options', required=False, default=DEFAULT_OPTIONS),
    )

    def render_tag(self, context, form, options):
        context.push()
        real_options = DEFAULT_OPTIONS.copy()
        real_options.update(options)
        context['form'] = self.prepare_form(form)
        context['fields'] = context['form']
        context['options'] = real_options
        prefix = self.render_prefix(context)
        postfix = self.render_postfix(context)
        content = loader.get_template('zenforms/zenform_inline.html').render(context)
        output = prefix + content + postfix
        context.pop()
        return output


class MultifieldTag(Tag):
    """
    ``{% multifield %}`` tag allows you to group fields in form.
    For example, first name and last name in your login form.

    **Usage** ::
        {% multifield args as varname [label 'Label'] %}
    """
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
        context[varname] = mf
        return u''


class FieldsetTag(Tag):
    """
    FieldsetTag renders fieldset with specified fields in it.

    **Usage:** ::

        {% fieldset 'field1' 'field2' [title 'MyFieldset'] %}
        {% fieldset unused_fields %}
    """
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
    template = 'zenforms/fields/readonly.html'
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

@register.filter
def widget_type(field):
    if isinstance(field, BoundField):
        return str(field.field.widget.__class__.__name__)

register.tag(ZenformTag)
register.tag(InlineZenformTag)
register.tag(MultifieldTag)
register.tag(FieldsetTag)
register.tag(Submit)
register.tag(ReadonlyTag)
