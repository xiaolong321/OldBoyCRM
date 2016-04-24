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


Page_Models = admin.models.Customer
Page_Admin = admin.CustomerAdmin

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


def get_customer_info(request, ret):
    pk = request.POST.get('pk', None)
    if pk is None:
        raise Exception('id 错误')
    Page = Page_Models.objects.get(id=pk)
    ret['results'] = []
    count = 0

    for i in Page_Admin.my_fieldsets:
        customer_info(i, ret, count, Page)
        count += 1
    ret['ret_code'] = 0
    logger.info(ret)
    return ret


def customer_info(i, ret, count, Page):
    try:
        data = []
        try:
            my_mode = i[1]['my_mode']
        except:
            my_mode = True
        for x in i[1]['fields']:
            field = Page_Models._meta.get_field(x)
            _description = Page_Models._meta.get_field(x)._description().split('：')[1]
            try:
                get_choices = Page_Models._meta.get_field(x).get_choices()
            except:
                get_choices = []
            if _description == 'ManyToManyField':
                _data = ['%s' % xxx for xxx in getattr(Page, x).all()]
            elif _description == 'ForeignKey':
                _data = "%s" % getattr(Page, x)
            elif _description == 'PositiveSmallIntegerField':
                for choices in get_choices:
                    if str(getattr(Page, x)) == str(choices[0]):
                        _data = choices[1]
            else:
                _data = "%s" % getattr(Page, x)
            if _data == 'None':
                _data = ''
            try:
                if x in i[1]['no_input']:
                    no_input = True
                else:
                    no_input = False
            except:
                no_input = False
            data.append(
                {
                    'name': field.verbose_name,
                    'type': _description,
                    'code': x,
                    'data': _data,
                    'get_choices': get_choices,
                    'no_input': no_input
                }
            )
        ret['results'].append(
            {
                'mode': my_mode,
                'code': "fieldsets_%s" % count,
                'title': i[0],
                'data': data
            }
        )
    except Exception as e:
        print e.message
        pass


def post_customer_info(request, ret):
    pk = request.POST.get('id', None)
    if pk is None:
        raise Exception('id 错误')
    try:
        Data = json.loads(request.POST.get('data', None))
        if Data is None:
            raise Exception('Data 没有数据')
    except Exception as e:
        raise Exception(u'Data json 错误!')
    user = request.POST.get('userName', None)
    if user is None:
        raise Exception('userName 错误')
    Page = Page_Models.objects.get(id=pk)
    logger.debug(
        u'id:%s data:%s' % (
            pk,
            json.dumps(Data)
        )
    )
    for k, v in Data.items():
        detail_info_save(k, v, Page)
    Page.creator = admin.models.UserProfile.objects.get(name=user)
    Page.save()
    ret['ret_code'] = 0
    return ret


def detail_info_save(k, v, Page):
    try:
        if not hasattr(Page, k):
            raise Exception(u'参数校验错误 !!!!')
        _description = Page._meta.get_field(k)._description().split('：')[1]
        if _description == 'CharField':
            setattr(Page, k, v)
        elif _description == 'ManyToManyField':
            Page_k = getattr(Page, k)
            Page_k.clear()
            print type(v)
            for vv in v:
                try:
                    objvv = Page._meta.get_field(k).remote_field.model.objects.get(id=vv)
                    print objvv
                    Page_k.add(objvv)
                except:
                    pass
        elif _description == 'PositiveSmallIntegerField':
            try:
                setattr(Page, k, Page._meta.get_field(k).related_model.objects.get(id=v))
            except:
                setattr(Page, k, v)
            pass
        elif _description == 'ForeignKey':
            setattr(Page, k, Page._meta.get_field(k).related_model.objects.get(id=v))
            pass
        else:
            raise Exception(u'尚未 计算类型')
        Page.save()
    except Exception as e:
        print e.message
        pass


def main():
    pass


if __name__ == '__main__':
    main()
