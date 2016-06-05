#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
import ansible.runner
# import MyConfig
import os

logger_linux = logging.getLogger(__name__)
# from backend.commons.log import logger_print as logger_My
import time


class ansible_filedescriptor(Exception):
    pass


def ansible_formal(
        module_args,
        host_list,
        module_name='shell',
        logger=logger_linux,
        r_user='work',
        r_pass='1a2s3dqwe',
        r_port='22',
        key_path='/',
        forks_num='3',
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
    count = 0
    while True:
        count += 1
        try:
            result = local_ansible_runner(
                module_args=module_args,
                host_list=host_list,
                module_name=module_name,
                r_user=r_user,
                r_pass=r_pass,
                r_port=r_port,
                key_path=key_path,
                forks_num=forks_num,
            )
        except:
            raise errorb(u'基础执行 时出错 请及时关注!!!')
        if result is None:
            raise Exception(u"没有任何内容")
        import pprint
        for ip, val in result['contacted'].items():
            print ip, val['ansible_facts']
        local_ansible_logs_contacted(result, logger, errorb=errorb)
        try:
            local_ansible_logs_dark(result, logger, errorb=errorb)
        except ansible_filedescriptor as e:
            logger.error(u'检测到 %s' % e.message)
            if count < 10:
                time.sleep(10)
                continue
            # 此处增加 重启检测内容
            cmd = u"""echo 'True'>/tmp/noah_client.logs"""
            os.popen(cmd).read()
            logger.error(u'超过最大抛错 次数 请及时处理')
            raise errorb(u'超过最大抛错 次数 请及时处理')
        logger.log(83, u'本次共执行主机%s台,其中成功%s台,失败%s台' % (
            len(host_list), len(result['contacted']), len(result['dark'])))
        return result


def local_ansible_runner(
        module_args,
        host_list,
        module_name='shell',
        r_user='work',
        r_pass='1a2s3dqwe',
        r_port='22',
        key_path='/',
        forks_num='3',
):
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
    return runner.run()


def local_ansible_logs_contacted(result, logger, errorb=Exception):
    """
        获取 ansbile contacted 内容
    """
    for (hostname, results) in result['contacted'].items():
        logger.debug(u'涉及主机信息:{ip:%s,user:%s,port:%s}' % (
            hostname,
            'work',
            '22'))
        logger.log(82, '*' * 50)
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
        logger.log(82, '*' * 50)


def local_check_logs(m, error):
    __check_list = [
        u'ValueError: filedescriptor out of range in select()'
    ]
    for i in __check_list:
        if m in i:
            raise ansible_filedescriptor(i)


def local_ansible_logs_dark(result, logger, errorb=Exception):
    for (hostname, results) in result['dark'].items():
        logger.log(
            82,
            u'涉及主机信息:{ip:%s,user:%s,port:%s}' % (
                hostname,
                'work',
                '22'
            )
        )
        logger.log(82, '*' * 50)
        msg = results['msg'].split('\n')
        del results['msg']
        logger_My(results, mode='error', logger=logger)
        logger_My({'msg': msg}, mode='error', logger=logger)
        results['msg'] = '\n'.join(msg)
        logger.log(82, '*' * 50)
        for m in msg:
            local_check_logs(m, error=ansible_filedescriptor)
        raise ansible_filedescriptor(u'拥有错误')


if __name__ == '__main__':
    # from backend.commons import log

    for i in xrange(1):
        aa = ansible_formal(
            module_name='setup',
            module_args='',
            host_list=['100.66.240.53'])
