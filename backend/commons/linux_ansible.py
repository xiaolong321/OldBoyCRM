#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
import ansible.runner

logger_linux = logging.getLogger(__name__)
from backend.commons.loggs import logger_print as logger_My



def ansible_formal(
        module_args,
        host_list,
        module_name='shell',
        logger=logger_linux,
        r_user='work',
        r_pass='1a2s3dqwe',
        r_port=22,
        # key_path=MyConfig.configration['key_path'],
        forks_num=3,
        errorb=Exception):
    """

    :param module_args:
    :param host_list:
    :param logger:
    :param module_name:
    :param r_user:
    :param r_pass:
    :param r_port:
    :param key_path:
    :param forks_num:
    :return:
    """
    runner = ansible.runner.Runner(
        host_list=host_list,
        module_name=module_name,
        module_args=module_args,
        remote_port=r_port,
        remote_user=r_user,
        remote_pass=r_pass,
        forks=forks_num,
        # private_key_file=key_path,
        environment={
            'LANG': 'zh_CN.UTF-8',
            'LC_CTYPE': 'zh_CN.UTF-8'
        }
    )
    result = runner.run()
    if result is None:
        raise Exception(u"No hosts found")
    for (hostname, results) in result['contacted'].items():
        logger.debug(u'涉及主机信息:{ip:%s,user:%s,port:%s}' % (
                         hostname,
                         'work',
                         22))
        logger.log(82, '*'*50)
        try:
            if results['rc'] == 0:
                stdout = results['stdout']
                del results['stdout']
                try:
                    stderr = results['stderr']
                    del results['stderr']
                except:
                    stderr = None
                    pass
                logger.log(81, results['cmd'])
                logger_My(results, mm=83, logger=logger)
                logger_My(data={'stdout': stdout}, mm=82, logger=logger)
                logger_My(data={'stderr': stderr}, mm=82, logger=logger)
                results['stdout'] = stdout
                try:
                    results['stderr'] = stderr
                except:
                    pass
            else:
                logger_My(results, mode='error', logger=logger)
                raise errorb(u'拥有错误')
        except:
            logger_My(results, mode='error', logger=logger)
            raise errorb(u'拥有错误')
        logger.log(82, '*'*50)
    for (hostname, results) in result['dark'].items():
        logger.log(82,u'涉及主机信息:{ip:%s,user:%s,port:%s}' % (
                         hostname,
                         'work',
                         22))
        logger.log(82, '*'*50)
        logger_My(results, mode='error', logger=logger)
        logger.log(82, '*'*50)
        raise errorb(u'拥有错误')
    logger.log(83,u'本次共执行主机%s台,其中成功%s台,失败%s台' % (
        len(host_list), len(result['contacted']), len(result['dark'])))
    return result


if __name__ == '__main__':
    aa = ansible_formal(
            module_args='ls -l',
            host_list=['100.66.240.150'])

