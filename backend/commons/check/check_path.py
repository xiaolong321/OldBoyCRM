#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import os
from backend.response.base_response import BaseResponse
import logging
logger = logging.getLogger(__name__)

def check_path_exist(log_abs_file):
    """
    检测是否存在logs文件夹.不存在则进行创建
    :param log_abs_file:logs文件夹
    :return:
    """
    response = BaseResponse()
    try:
        log_path = os.path.split(log_abs_file)[0]
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        response.status = True
    except Exception as e :
        response.message = e.message
        response.status = False
    return response