#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'

import logging

logger = logging.getLogger(__name__)

from backend.decorators.api_auth import api_auth_check
from .Customer import Customer_views
p_object = {
    "crm_customer": {
        'object': Customer_views,
        'Whitelist': [
            {
                'name': 'customer 方法',
                'func': 'customer_list',
                'type': ['get'],
                'memo': '获取 customer_list 列表方法'
            },
            {
                'name': 'customer_info 方法',
                'func': 'customer_info',
                'type': ['get', 'post'],
                'memo': '获取 customer_info 文件内容方法'
            },
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
