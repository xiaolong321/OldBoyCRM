#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging

logger = logging.getLogger(__name__)


def print_logs(My_modes):
    def _deco(func):
        def __deco(*args, **kwargs):
            logger.info(
                My_modes.Config.logs_name +
                "args:%s kwargs:%s" % (args, kwargs)
            )
            ret = func(*args, **kwargs)
            logger.info(
                My_modes.Config.logs_name +
                "func_name:%s data: %s" % (func.__name__, ret)
            )
            return ret

        return __deco

    return _deco


def logger_print(data, logger=logger, mode='info', k=None, mm=None):
    # TODO 此为临时方法. 需要编写一个固定方法...用于打印报错详细信息....
    """
    :param data:
    :param logger:
    :param mode:
    :return:
    """
    if type(data) == list:
        for v in data:
            logger_print(v, logger, mode, k, mm)
    elif type(data) == dict:
        for k, v in data.items():
            if v:
                logger_print(v, logger, mode, k, mm)
    else:
        if mm is None:
            getattr(logger, mode)(u'%s:%s' % (k, data))
        else:
            try:
                for i in data.split('\n'):
                    if len(i) != 0:
                        logger.log(mm, u'%s:%s' % (k, i))
            except:
                logger.log(mm, u'%s:%s' % (k, data))
def main():
    pass


if __name__ == '__main__':
    main()
