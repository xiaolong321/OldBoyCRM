#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'

import logging

logger = logging.getLogger(__name__)

from django.shortcuts import HttpResponse
from core.adminlte import middleware
import json
import datetime
from datetime import date
from . import crm_customer


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


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
                result = json.dumps(ret, cls=CJsonEncoder)
                logger.info(u'logs_data:%s result:%s' % (logs_data, result))
                return HttpResponse(result)

            # 返回值
            ret = {
                'action': None,
                'ret_code': 1,
                "ret_count": 0
            }
            try:
                # 获取 action
                action = request.POST.get('action', None)
                if action is None:
                    ret['action'] = 'error'
                    ret['ret_code'] = 1
                    ret['message'] = u'# action 您没有这个接口权限.'
                    return my_HttpResponse(
                        ret,
                        logs_data=ret['message'],
                    )
                # 获取 action_name 进行类型判断
                action_name = request.POST.get('action_name', None)
                if action_name is None or action_name not in p_object.keys():
                    ret['action_name'] = 'None'
                    ret['ret_code'] = 1
                    ret['message'] = u'# action_name:%s 您没有这个接口权限' % action_name
                    return my_HttpResponse(
                        ret,
                        logs_data=ret['message']
                    )
                # 判断是否存在相应的 接口.
                if hasattr(p_object[action_name]['object'], action) == False or \
                                action not in p_object[action_name]['Whitelist']:
                    # 表达式 1 action 不能在 action_name 中可以进行调用. 为True
                    # 表达式 2 action 不在可被调用白名单中. 为True
                    ret['action'] = 'error'
                    ret['ret_code'] = 1
                    ret['message'] = u'# action:%s ,action_name:%s 您没有这个接口权限.' % (action, action_name)
                    return my_HttpResponse(
                        ret,
                        logs_data=ret['message']
                    )
                ret['action'] = action
                ret = getattr(p_object[action_name]['object'], action)(request, ret)
                ret = func(ret)
            except Exception as e:
                print e
            return my_HttpResponse(
                ret,
                logs_data=''
            )

        return wrapper

    return _deco


p_object = {
    "crm_customer": {
        'object': crm_customer,
        'Whitelist': [
            'get_list_crm_customer',
        ]
    },
}


@api_auth_check(p_object)
def chuliqi(ret):
    """
    参数 ret 是全局返回值
    :param ret:
    :return:
    """
    return ret
    pass


def main():
    pass


if __name__ == '__main__':
    main()
