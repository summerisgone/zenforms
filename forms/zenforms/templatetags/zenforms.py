# -*- coding: utf-8 -*-
from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiValueArgument
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
        MultiValueArgument('fields'),
        'title',
        Argument('title', required=False),
    )
    template = 'zenforms/fieldset.html'

    def udpate_context(self, field, form, tag_context, unused_fields):
        if ',' in field:
            multifield = []
            for fname in [e.strip() for e in field.split(',')]:
                try:
                    multifield.append(form[fname])
                    unused_fields.remove(fname)
                except KeyError:
                    raise TemplateError('form does not contain field %s' % field)

            tag_context['fields'].append(multifield)
        else:
            try:
                tag_context['fields'].append(form[field])
                unused_fields.remove(field)
            except KeyError:
                raise TemplateError('form does not contain field %s' % field)

    def get_context(self, context, title, fields):
        tag_context = {'fields': [], 'title': title}
        try:
            form = context['form']
            unused_fields = context['unused_fields']
        except KeyError:
            raise TemplateError('fieldset tag must be used in {% zenform %}{% endzenform %} context')
        for field in fields:
            # TODO: Обработка списка полей
            self.udpate_context(field, form, tag_context, unused_fields)
        context.update(tag_context)
        return context

    def render_tag(self, context, title, fields):
        context = self.get_context(context, title, fields)
        template = loader.get_template(self.template)
        output = template.render(context)
        return output


register.tag(Zenform)
register.tag(Fieldset)