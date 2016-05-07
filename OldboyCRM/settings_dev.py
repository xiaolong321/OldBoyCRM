#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *

print u"^" * 20 + u'测试环境' + u"^" * 20
DEBUG = True
SHELL_MODE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'logs', 'dev_db.sqlite3'),
    }
}

############################################
# for i in LOGGING['handlers']:
#     LOGGING['handlers'][i]['level'] = 'DEBUG'
