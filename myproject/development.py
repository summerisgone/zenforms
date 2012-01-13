from forms.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG

INSTALLED_APPS += ['debug_toolbar',]

INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES += [
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
