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

from core.adminlte.web_models import myauth
import core.crm.web_api.issus
INSTALLED_API_OBJ = (
    'core.web_asset.my_api.api_views',
)


if __name__ == '__main__':
    for i in INSTALLED_API_OBJ:
        try:
            for k, v in core.crm.web_api.issus.p_object.items():
                k_dict = {
                             "action_name": k,
                             "memo": '自动添加',
                         }
                try:
                    k_obj = myauth.Permission_Api_objects.objects.create(**k_dict)
                except:

                    k_obj = myauth.Permission_Api_objects.objects.get(action_name=k)
                for i in v['Whitelist']:
                    try:
                        for x in i['type']:
                            try:
                                if myauth.Permission_Api_Action.objects.filter(
                                        action= i['func'],
                                        Type=myauth.RequestType.get_code(name=x)
                                ):
                                    continue
                                myauth.Permission_Api_Action.objects.create(
                                    **{
                                        'action_objects': k_obj,
                                        'action': i['func'],
                                        'Type': myauth.RequestType.get_code(name=x),
                                        'memo': '自动添加 %s 方法 %s 中的请求:%s ' % (
                                            k, i['name'], x
                                        ),
                                    }
                                )
                            except Exception as e :
                                print e.message
                                pass
                    except:
                        pass

        except Exception as e:
            print e.message
            pass
    pass
