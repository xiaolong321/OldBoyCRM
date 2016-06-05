#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'

import logging

logger = logging.getLogger(__name__)

from backend.decorators.api_auth import api_auth_check
from .classlist import views as classlist_views

common_list = {
    'name': 'search 方法',
    'func': 'search',
    'type': ['get'],
    'memo': '获取 查询列表 列表方法'
}
common_detail = {
    'name': 'detail 方法',
    'func': 'detail',
    'type': ['get', 'post'],
    'memo': '获取 detail 详细内容信息 文件内容方法'
}
common_add = {
    'name': 'common_add 方法',
    'func': 'common_add',
    'type': ['post'],
    'memo': '获取 common_add 文件内容方法'
}
p_object = {
    "classlist": {
        'object': classlist_views,
        'Whitelist': [
            common_list,
            common_detail,
            common_add,
            {
                'name': 'modify 方法',
                'func': 'modify',
                'type': ['get', 'post'],
                'memo': '获取 common_add 文件内容方法'
            },
            {
                'name': 'info 方法',
                'func': 'info',
                'type': ['get'],
                'memo': '获取 info 文件内容方法'
            }
        ]
    }
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
