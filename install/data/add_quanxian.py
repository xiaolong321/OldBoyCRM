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
from core.crm.web_api import issus as web_api
INSTALLED_API_OBJ = (
    'core.web_asset.my_api.api_views',
)

def mian(objs):
    try:
        for k, v in getattr(objs,'p_object').items():
            print k
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
                    if i['type']:
                        print i
                        for x in i['type']:
                            try:
                                if myauth.Permission_Api_Action.objects.filter(
                                        action_objects=k_obj,
                                        action=i['func'],
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
                            except Exception as e:
                                print e.message
                    else:
                        try:
                            if myauth.Permission_Api_Action.objects.filter(
                                    action_objects=k_obj,
                                    action=i['func'],
                            ):
                                continue
                            myauth.Permission_Api_Action.objects.create(
                                **{
                                    'action_objects': k_obj,
                                    'action': i['func'],
                                    'memo': '自动添加 %s 方法 %s ' % (
                                        k, i['name']
                                    ),
                                }
                            )
                        except Exception as e:
                            print e.message
                except Exception as e:
                    print e.message
                    pass

    except Exception as e:
        print e.message
        pass



if __name__ == '__main__':
    mian(web_api)