#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from django.http import HttpResponse
from core.adminlte.web_models.models import Permission, Menu
from backend.commons.list_paixu_quchong import list_qc
import logging

logger = logging.getLogger(__name__)
import json
from backend.commons import serialization
from django.utils.safestring import SafeString

__author__ = 'lyhapple'


class ApiPermissionCheck(object):
    def process_request(self, request):
        if not request.user.is_superuser \
                and request.path_info.startswith('/api/v1/'):
            # todo: cache
            permissions = Permission.objects.filter(
                group__in=request.user.groups.all()
            )
            resources = [
                list(p.resources.values_list('url', flat=True))
                for p in permissions
                ]
            for List in resources:
                if type(List) != list:
                    if str(request.path_info) != str(List):
                        return HttpResponse(status=403)
                else:
                    if request.path_info not in List:
                        return HttpResponse(status=403)


class MenuMiddleware(object):
    def process_template_response(self, request, response):
        # todo: cache
        logger.debug(
            u'*' * 5 + u'Menu 整理' +u'*' * 5 +
            u'用户:%s 当前状态:%s' % (
                request.user,
                u'开始'
            )
        )
        response.context_data['page_menus'] = []
        response.context_data['groups'] = []
        if request.path_info.startswith('/page/') \
                or request.path_info.startswith('/crm/') \
                or request.path_info == '/':
            if request.user.is_superuser:
                page_menus = Menu.objects.filter(status=Menu.USABLE)
                groups = []
            else:
                groups = request.user.groups.all()
                page_menus = []
                for i in groups:
                    permission = Permission.objects.filter(
                        group=i
                    ).first()
                    try:
                        page_menus += permission.menus.filter(status=Menu.USABLE)
                    except:
                        pass
            response.context_data['page_menus'] = Get_Ztrees(list_qc(page_menus), request.path_info)
            response.context_data['groups'] = list_qc(groups)
            logger.debug(
                u'*' * 5 + u'Menu 整理' + u'*' * 5 +
                u'用户:%s 管理员:%s 菜单数量:%s' % (
                    request.user,
                    request.user.is_superuser,
                    len(page_menus)
                )
            )

        logger.debug(
            u'*' * 5 + u'Menu 整理' + u'*' * 5 +
            u'用户:%s 当前状态:%s' % (
                request.user,
                u'结束'
            )
        )
        return response

def Get_Ztrees(page_menus, url):
    """
        分解 page_menus 并标记 url
    """
    # 分解 page_menus 并解析成字典方式
    def add_children_file(Menu):
        """
            添加 children_dir方法 并返回相关的 add_list
        """
        __children = {
            "id": Menu.id,
            "json": Menu,
            'children': []
        }
        return __children

    def add_children_dir(Main, children_list):
        """
            添加 children_file方法
        """
        children_list.append(Main)

    def check_children_list(ParentId, Menus):
        """
            循环 children_list 检测 path 是否存在 存在 则返回相应的内容
        """
        # logger.debug(
        #     u'#' * 2 +
        #     u"检测 PATH 是否存在于 children_list 中" +
        #     u"循环 children_list "
        # )
        for i in Menus:
            if unicode(ParentId) == unicode(i['id']):
                i.setdefault('children', [])
                return i
            try:
                __check = check_children_list(ParentId, i['children'])
                if not __check:
                    continue
                else:
                    __check.setdefault('children', [])
                    return __check
            except Exception as e:
                continue
        return False

    menus = []
    logger.debug(u'#' * 15 + u"循环 page_menus 所涉及的配置")
    for menu in page_menus:
        if menu.parent is None:
            logger.debug(u'#' * 5 + u"检测到menu:%s 为一级标签" % menu.name)
            add_children_dir(
                add_children_file(Menu=menu),
                children_list=menus
            )
            continue
        ___children = check_children_list(
            ParentId=menu.parent.id,
            Menus=menus
        )
        logger.debug(
            u'#' * 5 +
            u"# 进行添加文件" +
            u"name:%s url:%s id:%s" % (menu.name, menu.url, menu.id)
        )
        add_children_dir(
            add_children_file(Menu=menu),
            children_list=___children.get('children', [])
        )
    logger.debug(u'#' * 15 + u"循环 menus 开始生成url")

    def add_a(Menu):
        if Menu['children']:
            href = 'javascript:void(0)'
            span = "<span>%s</span>" % Menu['json'].name
            i_2 = '<i class="fa fa-angle-left pull-right"></i>'
        else:
            href = Menu['json'].url
            span = "%s" % Menu['json'].name
            i_2 = ''
        i_1 = '<i class="fa %s"></i>' % Menu['json'].icon
        return """<a href="%s">%s%s%s</a>""" % (
            href,
            i_1,
            span,
            i_2,
        )
        pass

    def add_li(Menu, active):
        if Menu['children']:
            li_1 = """<li class="treeview %s ">""" % check_me_open(Menu, url)
            A = add_a(Menu)
            Ul = add_ul(Menu, active)
            li_2 = """</li>"""
        else:
            if check_me_open(Menu, url):
                li_1 = """<li class="%s">""" % check_me_open(Menu, url)
            else:
                li_1 = """<li>"""
            A = add_a(Menu)
            li_2 = """</li>"""
            Ul = ''
        return "%s%s%s%s" %(
            li_1,
            A,
            Ul,
            li_2,
        )
        pass

    def add_ul(Menu, open):
        u_1 = """<ul class="treeview-menu">"""
        u_2 = []
        u_3 = "</ul>"
        for i in Menu['children']:
            u_2.append(add_li(i, open))
        return "%s%s%s" %(
            u_1,
            "".join(u_2),
            u_3
        )

    def check_me_open(me, url):
        if me['children']:
            for ii in me['children']:
                if check_me_open(ii, url):
                    return "active"
            return ''
        if me['json'].url == url:
            return "active"
        return ''

    ME = []
    for me in menus:
        ME.append(add_li(me,''))
    return "".join(ME)