# -*- coding: utf-8 -*-
from classytags.core import Tag, Options
from classytags.arguments import Argument
from django import template
from django.template import loader


register = template.Library()

class TemplateError(Exception):
    pass

class Zenform(Tag):
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


class Fieldset(Tag):
    name = 'fieldset'
    options = Options(
        Argument('title'),
        Argument('fields')
    )
    template = 'zenforms/fieldset.html'

    def split_fields(self, fields_str):
        fields = [e.strip() for e in fields_str.split(',')]
        return fields

    def get_context(self, context, title, fields_str):
        tag_context = {'fields': [], 'title': title}
        try:
            form = context['form']
            unused_fields = context['unused_fields']
        except KeyError:
            raise TemplateError('fieldset tag must be used in {% zenform %}{% endzenform %} context')
        fields = self.split_fields(fields_str)
        for field in fields:
            try:
                tag_context['fields'].append(form[field])
                unused_fields.remove(field)
            except KeyError:
                raise TemplateError('form does not contain field %s' % field)
        context.update(tag_context)
        return context

    def render_tag(self, context, title, fields):
        context = self.get_context(context, title, fields)
        template = loader.get_template(self.template)
        output = template.render(context)
        return output


register.tag(Zenform)
register.tag(Fieldset)