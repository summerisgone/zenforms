from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('')
admin.autodiscover()

if settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT}),
#    )
    urlpatterns += staticfiles_urlpatterns()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url('^', include('example.urls')),
)

