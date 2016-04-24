#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
import ldap
import hashlib

logger = logging.getLogger(__name__)

'''
实现LDAP用户登录验证，首先获取用户的dn，然后再验证用户名和密码
'''
# 登陆 地址
LDAP_HOST = '100.66.240.151'
# 登陆 账户
ldapuser = 'cn=admin,dc=jxjr,dc=com'
# 登陆 密码
ldappass = 'ssss'
# 默认 区域
BASE_DN = 'DC=jxjr,DC=com'


class LDAPTool(object):
    def __init__(self,
                 ldap_host=None,
                 base_dn=None,
                 user=None,
                 password=None):
        """
        初始化
        :param ldap_host: hosts
        :param base_dn: 区域
        :param user: 默认用户
        :param password: 默认密码
        :return:
        """
        if not ldap_host:
            ldap_host = LDAP_HOST
        if not base_dn:
            self.base_dn = BASE_DN
        if not user:
            self.admin_user = ldapuser
        if not password:
            self.admin_password = ldappass
        try:
            self.ldapconn = ldap.open(ldap_host)
            self.ldapconn.simple_bind(self.admin_user, self.admin_password)
        except ldap.LDAPError, e:
            print e

    def ldap_search_dn(self, uid=None):
        """
        # 根据表单提交的用户名，检索该用户的dn,一条dn就相当于数据库里的一条记录。
        # 在ldap里类似cn=username,ou=users,dc=gccmx,dc=cn,验证用户密码，必须先检索出该DN
        :param uid: 用户 id
        :return:
        """
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "cn=" + uid

        try:
            ldap_result_id = obj.search(
                base=self.base_dn,
                scope=searchScope,
                filterstr=searchFilter,
                attrlist=retrieveAttributes
            )
            result_type, result_data = obj.result(ldap_result_id, 0)
            # import pprint
            # pprint.pprint(result_data)
            # [('cn=xuebk,ou=\xe6\x8a\x80\xe6\x9c\xaf\xe9\x83\xa8,dc=jxjr,dc=com',
            #   {'cn': ['xuebk'],
            #    'displayName': ['\xe8\x96\x9b\xe4\xbf\x9d\xe5\xba\x93'],
            #    'mail': ['xuebk@jxjr.com'],
            #    'objectClass': ['inetOrgPerson'],
            #    'sn': ['xuebk'],
            #    'title': ['13'],
            #    'userPassword': ['xuebk!@#$']})]
            if result_type == ldap.RES_SEARCH_ENTRY:
                return result_data
            else:
                return None
        except ldap.LDAPError, e:
            print e

    def ldap_get_user(self, uid=None):
        """
        查询 用户 .返回 用户绝对 uid 下的信息
        :param uid:
        :return:
        """
        result = None
        try:
            search = self.ldap_search_dn(uid=uid)
            if search is None:
                raise Exception(u'未查询到相应 id')
            for user in search:
                if user[1]['cn'][0] == uid:
                    result = {
                        'dn': user[0],
                        'cn': user[1]['cn'][0],
                        'displayName': user[1]['displayName'][0],
                        'mail': user[1]['mail'][0],
                        'objectClass': user[1]['objectClass'][0],
                        'sn': user[1]['sn'][0],
                        'title': user[1]['title'][0],
                        'userPassword': user[1]['userPassword'][0],
                    }
            return result
        except ldap.LDAPError, e:
            print e

    def ldap_get_vaild(self, uid=None, passwd=None):
        """
        验证 用户名 密码是否一致
        :param uid:
        :param passwd:
        :return:
        """
        obj = self.ldapconn
        target_cn = self.ldap_get_user(uid=uid)
        try:
            if target_cn is None:
                return False
            if obj.simple_bind_s(target_cn['dn'], passwd):
                return True
            else:
                return False
        except ldap.LDAPError, e:
            print e
            return False

    def ldap_get_vaild_raise(self, uid=None, passwd=None):
        """
        验证 用户名 密码是否一致
        :param uid:
        :param passwd:
        :return:
        """
        obj = self.ldapconn
        target_cn = self.ldap_get_user(uid=uid)
        try:
            if target_cn is None:
                raise Exception(u'未查询到相应 id')
            if obj.simple_bind_s(target_cn['dn'], passwd):
                return True
            else:
                return False
        except ldap.LDAPError, e:
            print e
            return False

    def ldap_update_pass(self, uid=None, oldpass=None, newpass=None):
        modify_entry = [(ldap.MOD_REPLACE, 'userpassword', newpass)]
        obj = self.ldapconn
        target_cn = self.ldap_get_user(uid=uid)
        try:
            if target_cn is None:
                raise Exception(u'未查询到相应 id')
            obj.simple_bind_s(target_cn['dn'], oldpass)
            obj.simple_bind_s(self.admin_user, self.admin_password)
            obj.passwd_s(target_cn['dn'], oldpass, newpass)
            return True
        except ldap.LDAPError, e:
            print e
            return False


def main():
    print LDAPTool().ldap_get_user('jinxin')
    pass


if __name__ == '__main__':
    main()
