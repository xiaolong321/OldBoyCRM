#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebaoku'

import MyConfig
import logging
import logging.handlers
import logging.config
from lib.commons.check.check_os import check_system
from lib.commons.check.check_path import check_path_exist
from lib.commons.response import BaseResponse
# logs日志存储位置.此位置.需要根据 MyConfig 配置中得logfile进行修改 默认不用修改
check_path_exist(MyConfig.os.path.join(MyConfig.BASE_DIR+'/logs/',))
logger = logging.getLogger(__name__)
stamdard_format = '[%(asctime)s][%(threadName)s:%(thread)d]' + \
                  '[task_id:%(name)s][%(filename)s:%(lineno)d] ' + \
                  '[%(levelname)s]- %(message)s'
simple_format = '[%(levelname)s][%(asctime)s]' + \
                '[%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,# this fixes the problem
    'formatters': {
        'standard': {#详细
            'format': stamdard_format
        },
        'simple': {#简单
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        'console':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',# 打印到前台
            'formatter': 'simple'
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': MyConfig.os.path.join(
                    MyConfig.BASE_DIR+'/logs/','all.log'),
            # 或者直接写路径：'c:\logs\all.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'lib.plugins.JX_dev': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'paramiko.transport': {
            'handlers': ['default','console'],
            'level': 'ERROR',
            'propagate': False
        },

    }
}
logging.config.dictConfig(LOGGING)
logger.info('It works!')
#配置自定义级别
logging.addLevelName(81,'paramiko_cmd')#远程cmd调用命令
logging.addLevelName(82,'paramiko_data')#远程cmd调用结果
logging.addLevelName(83,'paramiko_status')#远程cmd调用结果
logging.addLevelName(91,'sub_cmd')#本地cmd调用命令
logging.addLevelName(92,'sub_data')#本地cmd调用结果
logging.addLevelName(93,'sub_status')#本地cmd调用结果
logging.addLevelName(101,'Update_All')#本地cmd调用结果


def my_addhandler(dir_path, name, log_ger, logs_file=None):
    try:
        system = check_system()
        if system.data == 'Linux':
            # logs_file = MyConfig.os.path.join(
            #     MyConfig.BASE_DIR+'/logs/' + \
            #     '%s'%dir,name+'.logs')
            logs_file = '/home/work/cmdb/logs/' + name
        elif system.data == 'Darwin':
            logs_file = MyConfig.os.path.join(
                    MyConfig.BASE_DIR + '/logs/' + \
                    '%s' % dir_path, name + '.logs')
        else:
            logs_file = MyConfig.os.path.join(
                    "C:\client_logs\\%s\\%s" % (dir_path, name + '.logs')
            )
            check_path_exist(MyConfig.os.path.join(
                    "C:\client_logs\\%s" % (dir_path)
            ))
        check_path_exist(logs_file)
        my_logger = logging.getLogger(name)
        my_logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(logs_file)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(id_simple_format)
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)
        #my_logger.addHandler(logger) #测试不能加入系统默认logger
        log_ger.debug(u'添加 自定义日志级别 成功')
        return my_logger
    except:
        log_ger.error(u'添加 自定义日志级别失败', exc_info=True)
        raise Exception(u'添加 自定义日志级别失败')

def My_removeHandler(name,logger):
    try:
        logger.removeHandler(name)
        logger.debug(u'删除 自定义日志级别 成功')
    except:
        logger.error(u'删除 自定义日志级别 失败',exc_info=True)
        raise Exception(u'删除 自定义日志级别 失败')

def logger_print(data, logger=logger, mode='info', k=None,mm=None):
        #TODO 此为临时方法. 需要编写一个固定方法...用于打印报错详细信息....
        """
        :param data:
        :param logger:
        :param mode:
        :return:
        """
        if type(data) == list:
            for v in data:
                logger_print(v,logger,mode,k,mm)
        elif type(data) == dict:
            for k,v in data.items():
                if v:
                    logger_print(v,logger,mode,k,mm)
        else:
            if mm is None:
                getattr(logger,mode)(u'%s:%s'%(k,data))
            else:
                try:
                    for i in data.split('\n'):
                        if len(i) != 0:
                            logger.log(mm, u'%s:%s'%(k,i))
                except:
                    logger.log(mm, u'%s:%s'%(k,data))