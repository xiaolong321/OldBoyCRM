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

Page_Admin = admin.ClassListAdmin
Page_Models = admin.models.ClassList

def get_common_list(request, ret):
    """
        获取 get_common_list 列表方法
     """
    # 获取相关的 search  page 等查询信息
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
    # 获取 总数.以及相关的具体内容
    all_count = get_common_list_count(
        conditions_key=conditions_key,
        conditions=conditions,
    )
    # 分页信息
    page_info = pager.PageInfo(page, all_count.count)
    # 分页后的详细 内容整形
    ret['results'] = get_common_list_results(page_info.start, page_info.end, data=all_count.data).data
    # 返回相关的分页信息
    ret["current_page"] = page_info.current_page
    ret["total_page"] = page_info.total_page
    ret["count"] = page_info.total_items
    ret['per_page'] = settings.REST_FRAMEWORK['PAGE_SIZE']
    # 最终判定是否成功. 在此之前 有错误需要直接抛错
    ret['ret_code'] = 0
    result = json.dumps(ret, cls=serialization.CJsonEncoder)
    logger.info(result)
    return ret


def get_common_list_count(**kwargs):
    """
    获取全部信息
    :param conditions:
    :return:
    """
    response = BaseResponse()
    response.count = 0
    try:
        # 查询接口整形
        # 利用 django的Q 方法 进行 .如果需要 可以自己写相关的查询 方法
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
        # 直接调用 django的 models  进行查询方式 这里默认采用 最新创建信息. 如果需要最近修改 .需要在增加一个字段
        obj = Page_Models.objects.filter(con).order_by("-id")
        response.count = obj.count()
        response.data = obj.values()
        response.status = True
    except Exception, e:
        print e.message
        response.message = str(e)
    return response


def get_common_list_results(start, end, data, **kwargs):
    """
    分页 之后.更改具体的单条值 信息 整形
    """
    response = BaseResponse()
    try:
        data = data[start:end]
        for i in data:
            get_common_list_ret_id(i)
        response.data = list(data)
        response.status = True
    except Exception, e:
        print e
        response.message = str(e)
    return response


def get_common_list_ret_id(data):
    '''
    具体 信息整形.可以添加或者是修改 相关字段
    '''
    try:
        Page_Models_id = Page_Models.objects.get(id=data['id'])
        try:
            list_display = Page_Admin.my_list_display
        except:
            list_display = Page_Admin.list_display
        for i in list_display:
            try:
                data[i] = "%s" % getattr(Page_Models_id,i)()
            except:
                data[i] = "%s" % getattr(Page_Models_id, i)
    except Exception, e:
        print e.message
    return data

def get_common_detail(request, ret):
    pass
def post_common_detail(request, ret):
    pass
def post_common_add(request, ret):
    pass