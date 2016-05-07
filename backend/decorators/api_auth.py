#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import HttpResponse
import time
import hashlib
import logging
import json
from backend.commons import serialization
from django.shortcuts import HttpResponse
from backend import middleware
from django.conf import settings
from core.adminlte.web_models.myauth import Permission_Api_objects, Permission_Api_Action, UsableStatus
from core.adminlte.web_models.constants import RequestType
logger = logging.getLogger(__name__)


def auth_api_valid(data):
    """ 用于API验证的方法 """
    try:
        encryption,time_span = data.split('|')
        time_span = float(time_span)
        if (time.time() - time_span) > settings.API_AUTH_RANGE:
            return False
        hash_obj = hashlib.md5()
        hash_obj.update("%s|%f" % (settings.API_KEY, time_span))
        if hash_obj.hexdigest() == encryption:
            return True
        else:
            return False
    except Exception,e:
        pass
    return False


# ########### 用于API验证的装饰器 ###########
def api_auth(func):
    """用于API验证的装饰器"""

    def wrapper(request):
        security_key = request.META.get('HTTP_SECURTYKEY',None)
        if not security_key:
            return HttpResponse('Unauthorized')
        if not auth_api_valid(security_key):
            return HttpResponse('Unauthorized')
        return func(request)
    return wrapper


def api_auth_check(p_object):
    """
    处理请求模块.按照请求.进行分类
    例:
    {
        "action": "GetEstimatedConsumption", # api 指令列表
        "root_user":"usr-GZIvqOJx" # 用户id 或者名称
    }
    :param request:
    :return:
    """
    def _deco(func):
        def wrapper(request):
            ApiPermissionCheck = middleware.ApiPermissionCheck()
            Check = ApiPermissionCheck.process_request(request)
            if Check is not None:
                return Check
            def my_HttpResponse(ret, logs_data=None):
                try:
                    result = json.dumps(ret, cls=serialization.CJsonEncoder)
                    logger.info(u'logs_data:%s result:%s' % (logs_data, result))
                    return HttpResponse(result)
                except:
                    return ret
            # 返回值
            ret = {
                    'action': None,
                    'ret_code': 1,
                    "ret_count": 0
                }
            try:
                Permission_Api_objects_list = [
                    i[0]
                    for i in Permission_Api_objects.objects.filter(
                        status=UsableStatus.USABLE).values_list('action_name')
                    ]
            except:
                Permission_Api_objects_list = []
            user_api_permissions_list = []
            if request.user.id is None:
                ret['action'] = 'error'
                ret['ret_code'] = 1
                ret['message'] = u'# 请从新进行登陆操作. '
                return my_HttpResponse(
                    ret,
                    logs_data=ret['message'],
                )
            try:
                for i in request.user.groups.filter(
                        groups__group_api_permissions__status=UsableStatus.USABLE
                    ).values_list('groups__group_api_permissions__action',
                                  'groups__group_api_permissions__Type'):
                    if i[1] is None:
                        user_api_permissions_list.append(
                            "%s" % i[0]
                        )
                    else:
                        user_api_permissions_list.append(
                            "%s_%s" % (RequestType.get_name(code=i[1]), i[0])
                        )
            except:
                user_api_permissions_list = []
            try:
                for i in request.user.user_api_permissions.filter(
                        status=UsableStatus.USABLE
                ).values_list('action', 'Type'):
                    if i[1] is None:
                        user_api_permissions_list.append(
                            "%s" % i[0]
                        )
                    else:
                        user_api_permissions_list.append(
                            "%s_%s" % (RequestType.get_name(code=i[1]), i[0])
                        )
            except:
                user_api_permissions_list += []
            try:
                # 获取 action
                # print Permission_Api_objects_list
                # print user_api_permissions_list
                action = request.POST.get('action', None)
                if action is None:
                    ret['action'] = 'error'
                    ret['ret_code'] = 1
                    ret['message'] = u'# action 没有值.'
                    return my_HttpResponse(
                        ret,
                        logs_data=ret['message'],
                    )
                # 获取 action_name 进行类型判断
                action_name = request.POST.get('action_name', None)
                if action_name is None or action_name not in Permission_Api_objects_list:
                    ret['action_name'] = 'None'
                    ret['ret_code'] = 1
                    ret['message'] = u'# action_name:%s 您没有这个接口权限' % action_name
                    return my_HttpResponse(
                        ret,
                        logs_data=ret['message']
                    )
                # 判断是否存在相应的 接口.
                if action not in user_api_permissions_list:
                    # 表达式 1 action 不能在 action_name 中可以进行调用. 为True
                    # 表达式 2 action 不在可被调用白名单中. 为True
                    ret['action'] = 'error'
                    ret['ret_code'] = 1
                    ret['message'] = u'# action:%s ,action_name:%s 您没有这个接口权限.' % (action, action_name)
                    return my_HttpResponse(
                        ret,
                        logs_data=ret['message']
                    )
                if hasattr(p_object[action_name]['object'], action) == False :
                    ret['action'] = 'error'
                    ret['ret_code'] = 1
                    ret['message'] = u'#反射 接口:%s 失败 ' % (action_name)
                    return my_HttpResponse(
                        ret,
                        logs_data=ret['message']
                    )
                # 权限判断
                ret['action'] = action
                ret = getattr(p_object[action_name]['object'], action)(request, ret)
                ret = func(ret)
            except Exception as e :
                print e
            return my_HttpResponse(
                        ret,
                        logs_data=''
                    )
        return wrapper
    return _deco