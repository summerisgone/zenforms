# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('example.views',
    url(r'^$', 'index', kwargs={'template_name': 'index.html'}, ),
    url(r'^zen/$', 'index', kwargs={'template_name': 'index_zen.html'}, ),
)