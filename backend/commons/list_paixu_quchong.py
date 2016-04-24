#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging

logger = logging.getLogger(__name__)


def list_qc(ids):
    """
    :param
    列表去重
    """
    func = lambda x, y: x if y in x else x + [y]
    try:
        return reduce(func, [[], ] + ids)
    except:
        return ids


def main():
    pass


if __name__ == '__main__':
    main()
