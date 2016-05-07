#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'

import logging

logger = logging.getLogger(__name__)

from backend.decorators.api_auth import api_auth_check
from .courserecord import views as courserecord_views
from .paymentrecord import views as paymentrecord_views
from .studyrecord import views as studyrecord_views
from .studentfaq import views as studentfaq_views
from .compliant import views as compliant_views
from .customer import views as customer_views
from .consultrecord import views as consultrecord_views
from .classlist import views as classlist_views
from .survery import views as survery_views
from .surveryitem import views as surveryitem_views
from .surveryrecord import views as surveryrecord_views

common_list = {
    'name': 'common_list 方法',
    'func': 'common_list',
    'type': ['get'],
    'memo': '获取 common_list 列表方法'
}
common_detail = {
    'name': 'common_detail 方法',
    'func': 'common_detail',
    'type': ['get', 'post'],
    'memo': '获取 customer_info 文件内容方法'
}
common_add = {
    'name': 'common_add 方法',
    'func': 'common_add',
    'type': ['post'],
    'memo': '获取 common_add 文件内容方法'
}
p_object = {
    "crm_courserecord": {
        'object': courserecord_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_paymentrecord": {
        'object': paymentrecord_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_studentfaq": {
        'object': studentfaq_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_compliant": {
        'object': compliant_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_customer": {
        'object': customer_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_consultrecord": {
        'object': consultrecord_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_classlist": {
        'object': classlist_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_survery": {
        'object': survery_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_surveryitem": {
        'object': surveryitem_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_surveryrecord": {
        'object': surveryrecord_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
        ]
    },
    "crm_studyrecord": {
        'object': studyrecord_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
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
