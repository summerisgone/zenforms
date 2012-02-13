# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('example.views',
    url(r'^$', 'index', kwargs={'template_name': 'index.html'}, name='index'),
    url(r'^zen/$', 'index', kwargs={'template_name': 'index_zen.html'}, name='index_zen'),
    url(r'^formset/$', 'profile', kwargs={'template_name': 'formset.html'}, name='formset'),
    url(r'^formset/zen/$', 'profile', kwargs={'template_name': 'formset_zen.html'}, name='formset_zen'),
)