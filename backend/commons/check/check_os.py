#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'

import platform
from backend.base_response import BaseResponse
import logging
logger = logging.getLogger(__name__)
def TestPlatform():
    logger.info("----------Operation System--------------------------")
    #Windows will be : (32bit, WindowsPE)
    #Linux will be : (32bit, ELF)
    logger.info(platform.architecture())

    #Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
    #Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
    logger.info(platform.platform())

    #Windows will be : Windows
    #Linux will be : Linux
    logger.info(platform.system())

    logger.info("--------------Python Version-------------------------")
    #Windows and Linux will be : 3.1.1 or 3.1.3
    logger.info(platform.python_version())

def check_system():
    response = BaseResponse()
    try:
        sysstr = platform.system()
        response.data = sysstr
        if response.data =="Windows":
            response.message = "Call Windows tasks"
        elif response.data == "Linux":
            response.message = "Call Linux tasks"
    except Exception as e :
        response.message = "Other System tasks \n%s"%(e.message)
        response.status = False
    return response

def check_platform():
    response = BaseResponse()
    try:
        sysstr = platform.platform()
        response.data = sysstr
        if response.data =="Windows":
            response.message = "Call Windows tasks"
        elif response.data == "Linux":
            response.message = "Call Linux tasks"
    except Exception as e :
        response.message = "Other System tasks \n%s"%(e.message)
        response.status = False
    return response

def check_python_version():
    response = BaseResponse()
    try:
        sysstr = platform.python_version()
        response.data = sysstr
        if response.data =="Windows":
            response.message = "Call Windows python"
        elif response.data == "Linux":
            response.message = "Call Linux python"
    except Exception as e :
        response.message = "Other System python \n%s"%(e.message)
        response.status = False
    return response
#check_system()