#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging

logger = logging.getLogger(__name__)
from core.adminlte.web_views.views import CommonPageViewMixin, TemplateView
from .. import admin


class Users(CommonPageViewMixin, TemplateView):
    # Page_Admin = admin.models_task.MsqlAdmin
    # Page_Models = admin.models_assets.BusinessUnit

    def get_context_data(self, **kwargs):
        """
        get 请求返回结果
        """
        context = super(Users, self).get_context_data(**kwargs)
        context['page_action_name'] = 'ProjectDev'
        return self.get_context_data_list(context, **kwargs)

    def get_context_data_list(self, context, **kwargs):
        from core.web_apps.my_models import constants
        Constants_SvnBase = constants.SvnBase
        self.template_name = 'assets/Users.html'  # 页面地址
        context['page_action'] = 'get_describe_list'

        context['page_title'] = '用户管理'
        # context['list_filter'] = [
        #     {
        #         'id': 'SvnBase',
        #         'verbose_name': 'SvnBase',
        #         'get_choices': Constants_SvnBase.get_STATUS(),
        #     }
        # ]
        context['list_display'] = [
            {'verbose_name': '账户名', 'id': 'name'},
            {'verbose_name': '用户组', 'id': 'groups', 'type': 'Dialog'},
            {'verbose_name': '权限', 'id': 'userpre', 'type': 'Dialog'},
            {'verbose_name': '操作', 'id': 'id'},
        ]
        context['list_display_buttons'] = [
            {
                'name': u'修改',
                'icon': 'fa-pencil-square-o',
                'type': 'get_modify',
                'action': 'get_modify'
            },
            {
                'name': u'详情',
                'icon': 'fa-sticky-note',
                'type': 'get_info',
                'action': 'get_info'
            },
            {
                "id": 'application',
                'icon': 'fa-space-shuttle fa-6',
                'name': u'应用',
                'type': 'application',
                'action': 'post_application'
            },
        ]
        context['all_list_display'] = [
            {
                "id": 'refresh',
                'icon': 'fa-refresh',
                'name': u'刷新',
                'type': 'search',
                'action': 'get_search'
            },
            {
                "id": 'adds',
                'icon': 'fa-plus-circle',
                'name': u'添加',
                'type': 'adds',
                'action': 'get_adds'
            },
            {
                "id": 'application',
                'icon': 'fa-space-shuttle',
                'name': u'应用全部',
                'type': 'application',
                'action': 'post_application'
            },
        ]
        context['search'] = True
        return context


def main():
    pass


if __name__ == '__main__':
    main()
