#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'logs', 'dev_db.sqlite3'),
    }
}

############################################
