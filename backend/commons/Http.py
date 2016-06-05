#!/usr/bin/env python
# encoding=UTF-8
import json
import logging
import requests

import MyConfig

# 本程序.用于 调用其他程序API使用. 作为requests 补充

# 下面是初始 声明
__author__ = 'xuebk'
__title__ = 'requests'
__version__ = '0.0.1'
__build__ = 0x000001
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 xbk'

# 本地函数.
logger_linux = logging.getLogger(__name__)  # 用于日志方法.


class Http_data():
    """
    返回值.调用
    """
    def __init__(self, data):
        self.ok = data


class HttpNetRobot:
    """
    模拟用户请求 方法
    """
    def __init__(self,
                 baseurl=None,
                 httpmode='http',
                 host=MyConfig.configration['host'],
                 port=MyConfig.configration['port'],
                 timeout=MyConfig.configration['timeout'],
                 logger=logger_linux,
                 user_name=None,
                 user_passwd=None,
                 ):

        if baseurl is None:
            baseurl = '%s://%s:%s' % (httpmode, host, port)
        self.baseurl = baseurl
        self.timeout = timeout
        self.logger = logger
        self.headerdata = {'Content-Type': 'application/text; charset=utf-8'}
        if user_name is not None and user_passwd is not None:
            s = requests.Session()
            s.auth = (user_name, user_passwd)
            s.headers.update({'x-test': 'true'})
            self.requests = s
        else:
            self.requests = requests

    def OPTIONS(self, requrl, mode=True):
        """

        按照 OPTIONS 进行请求

        :requrl url: 传入的url
        :mode  自动拼接
        :return: :class:`Response <Response>` object
        """
        if mode:
            requrl = self.baseurl + requrl
        self.logger.debug("%s%s%s%s%s%s" % (
            '=' * 25, 'OPTIONS', '=' * 2,
            requrl,
            '=' * 2, '=' * 25))
        try:
            res_data = self.requests.options(requrl, timeout=self.timeout)
            try:
                self.logger.debug("urllib2>>>>status_code:%s data:%s" % (
                        res_data.status_code,
                        json.dumps(res_data.json())))
            except:
                self.logger.debug("urllib2>>>>status_code:%s data:%s" % (
                        res_data.status_code,
                        json.dumps(res_data.text)))
            self.logger.debug("%s%s%s%s%s%s" % (
                '=' * 25, 'OPTIONS', '=' * 2,
                'success',
                '=' * 2, '=' * 25))
            return res_data
        except Exception as e:
            self.logger.error("%s%s%s%s%s%s" % (
                '=' * 25, 'OPTIONS', '=' * 2,
                'failure',
                '=' * 2, '=' * 25))
            return Http_data(False)

    def POST(self, requrl, post_data, mode=True):
        if mode:
            requrl = self.baseurl + requrl
        self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'POST', '=' * 2, requrl, '=' * 2, '=' * 25))
        try:
            res_data = self.requests.post(requrl, post_data, timeout=self.timeout)
            try:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.json())))
            except:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.text)))
            self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'POST', '=' * 2, 'success', '=' * 2, '=' * 25))
            return res_data
        except Exception as e:
            self.logger.error("%s%s%s%s%s%s" % ('=' * 25, 'POST', '=' * 2, 'failure', '=' * 2, '=' * 25))
            return Http_data(False)

    def GET(self, requrl, mode=True):
        if mode:
            requrl = self.baseurl + requrl
        self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'GET', '=' * 2, requrl, '=' * 2, '=' * 25))
        try:
            res_data = self.requests.get(requrl, timeout=self.timeout)
            try:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.json())))
            except:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.text)))
            self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'GET', '=' * 2, 'success', '=' * 2, '=' * 25))
            return res_data
        except Exception as e:
            self.logger.error("%s%s%s%s%s%s" % ('=' * 25, 'GET', '=' * 2, 'failure', '=' * 2, '=' * 25))
            return Http_data(False)

    def DELETE(self, requrl, mode=True):
        if mode:
            requrl = self.baseurl + requrl
        self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'DELETE', '=' * 2, requrl, '=' * 2, '=' * 25))
        try:
            res_data = self.requests.delete(requrl, timeout=self.timeout)
            try:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.json())))
            except:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.text)))
            self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'DELETE', '=' * 2, 'success', '=' * 2, '=' * 25))
            return res_data
        except Exception as e:
            self.logger.error("%s%s%s%s%s%s" % ('=' * 25, 'DELETE', '=' * 2, 'failure', '=' * 2, '=' * 25))
            return Http_data(False)

    def PUT(self, requrl, post_data, mode=True):
        if mode:
            requrl = self.baseurl + requrl
        self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'PUT', '=' * 2, requrl, '=' * 2, '=' * 25))
        try:
            res_data = self.requests.put(requrl, post_data, timeout=self.timeout)
            try:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.json())))
            except:
                self.logger.debug(
                    "urllib2>>>>status_code:%s data:%s" % (res_data.status_code, json.dumps(res_data.text)))
            self.logger.debug("%s%s%s%s%s%s" % ('=' * 25, 'PUT', '=' * 2, 'success', '=' * 2, '=' * 25))
            return res_data
        except Exception as e:
            self.logger.error("%s%s%s%s%s%s" % ('=' * 25, 'PUT', '=' * 2, 'failure', '=' * 2, '=' * 25))
            return Http_data(False)
