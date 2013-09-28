import os
from .common import SITE_ROOT

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(SITE_ROOT, 'var', 'db', 'database-dev.sqlite')),
        'HOST': '',
        'PORT': '',
    }
}
