#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OldboyCRM.settings")
logger = logging.getLogger(__name__)
import django
from django.core import serializers

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


def bulk_create(f, obj):
    BlogList = []
    for parts in f:
        try:
            obj.objects.bulk_create(
                [obj(**parts)]
            )
        except Exception as e:
            print e
            pass


def menu_dumpdata():
    from core.adminlte import admin as web_apps_admin

    obj = web_apps_admin.models.Menu
    obj = web_apps_admin.models.SystemConfig
    obj = web_apps_admin.models.Resource
    obj = web_apps_admin.models.Permission
    obj = web_apps_admin.models.Groups
    obj = web_apps_admin.models.UserProfile
    print serializers.serialize('json', obj.objects.all())


def dump_file(obj, file_name):
    from django.core import serializers
    output = open(file_name, 'w')
    objs = serializers.serialize('json', obj.objects.all())
    output.write(objs)
    output.close()


def load_file(obj, file_name):
    from django.core import serializers
    output = eval(open(file_name, 'r').read())
    try:
        bulk_create(output, obj)
    except:
        pass


if __name__ == '__main__':
    menu_dumpdata()
    pass
