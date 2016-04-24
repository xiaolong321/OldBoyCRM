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
        response.context_data['page_menus'] = []
        response.context_data['groups'] = []
        if request.path_info.startswith('/page/') \
           or request.path_info.startswith('/apps/') \
           or request.path_info.startswith('/assets/') \
           or request.path_info.startswith('/qy/') \
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
            response.context_data['page_menus'] = list_qc(page_menus)
            response.context_data['groups'] = list_qc(groups)
            logger.debug(u'user:%s is_admin:%s page_menus:%s' % (
                request.user,
                request.user.is_superuser,
                page_menus
            ))
        return response