#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
import json
from backend.base_response import BaseResponse_new as BaseResponse
from backend.commons import serialization
from backend.commons import pager
from django.conf import settings
from django.core import serializers
from django.db.models import Q

logger = logging.getLogger(__name__)
from core.crm import admin

Page_Admin = admin.CustomerAdmin
Page_Models = admin.models.Customer


def get_customer_list(request, ret):
    """
    获取 customer_list 列表方法
    """
    conditions = request.POST.get('search', None)
    page = request.GET.get('page', None)
    if not conditions:
        conditions = "{}"
    conditions = json.loads(conditions)
    conditions_key = request.POST.get('search_key', None)
    if not conditions_key:
        conditions_key = "{}"
    conditions_key = json.loads(conditions_key)

    logger.info("conditions:%s,conditions_key:%s,page:%s" % (
        conditions,
        conditions_key,
        page,
    ))
    all_count = get_customer_list_count(
        conditions_key=conditions_key,
        conditions=conditions,
    )
    page_info = pager.PageInfo(page, all_count.count)

    ret['results'] = get_customer_list_results(page_info.start, page_info.end, data=all_count.data).data
    ret["current_page"] = page_info.current_page
    ret["total_page"] = page_info.total_page
    ret["count"] = page_info.total_items
    ret['per_page'] = settings.REST_FRAMEWORK['PAGE_SIZE']
    ret['ret_code'] = 0
    result = json.dumps(ret, cls=serialization.CJsonEncoder)
    logger.info(result)
    return ret


def get_customer_list_count(**kwargs):
    """
    获取全部信息
    :param conditions:
    :return:
    """
    response = BaseResponse()
    response.count = 0
    try:
        con = Q()
        for k, v in kwargs['conditions'].items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con.add(temp, 'AND')

        for k, v in kwargs['conditions_key'].items():
            k = k.split('.')[-1]
            temp = Q()
            temp.connector = 'AND'
            if v is None:
                continue
            if len(v) == 0:
                continue
            if v == '9999':
                continue
            temp.children.append((k, v))
            con.add(temp, 'AND')

        logger.info(u'con_Q:%s' % (
            con
        ))

        obj = Page_Models.objects.filter(con).order_by("-id")
        response.count = obj.count()
        response.data = obj.values()
        response.status = True
    except Exception, e:
        print e.message
        response.message = str(e)
    return response


def get_customer_list_results(start, end, data, **kwargs):
    response = BaseResponse()
    try:

        data = data[start:end]
        for i in data:
            ret_customer_list_id(i)
        response.data = list(data)
        response.status = True
    except Exception, e:
        print e
        response.message = str(e)
    return response


def ret_customer_list_id(data):
    try:
        Page_Models_id = Page_Models.objects.get(id=data['id'])
        try:
            data['colored_status'] = Page_Models_id.colored_status()
        except:
            data['colored_status'] = ''
        try:
            data['get_enrolled_course'] = Page_Models_id.get_enrolled_course()
        except:
            data['get_enrolled_course'] = ''
    except Exception, e:
        print e.message
    return data

def main():
    pass


if __name__ == '__main__':
    main()
