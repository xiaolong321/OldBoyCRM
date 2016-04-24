#!/usr/bin/env python
# -*- coding:utf-8 -*-

class BaseResponse(object):
    def __init__(self):
        self.status = False
        self.message = ''
        self.data = None


class BaseResponse_new(object):
    """
    底层类.用于标准化
    """

    def __init__(self):
        self.__status = False  # 默认不会有任何返回
        self.__message = ''  # 消息
        self.__data = None  # 具体内容

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value
