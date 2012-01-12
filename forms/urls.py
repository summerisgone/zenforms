from django.conf.urls.defaults import *
from django.conf import settings
from staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()


urlpatterns = patterns('',
)

