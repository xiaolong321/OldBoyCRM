#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging

logger = logging.getLogger(__name__)
from core.adminlte.web_views.views import CommonPageViewMixin, TemplateView
from core.crm.web_models import constants
from core.adminlte.web_models import models


class Views(CommonPageViewMixin, TemplateView):
    def get_context_data(self, **kwargs):
        """
        get 请求返回结果
        """
        context = super(Views, self).get_context_data(**kwargs)
        # 调用的 api 的 action_name
        # 没有生效 .去 js里面改.action_name 即可
        context['page_action_name'] = 'customer'
        add = self.request.GET.get('add', None)
        Pk = self.request.GET.get('pk', None)
        if add:
            print context, kwargs
            return self.get_context_add(context, **kwargs)
        if Pk:
            return self.get_context_Pk(context, Pk, **kwargs)
        return self.get_context_data_list(context, **kwargs)

    def get_context_data_list(self, context, **kwargs):
        self.template_name = 'crm/customer_list.html'  # 页面地址
        context['page_action'] = 'get_describe_list'

        context['page_title'] = '客户信息'
        # 自定义 类搜索
        # 这里可以直接从后端获取相关的搜索主键
        context['list_filter'] = [
            {
                'id': 'source',
                'verbose_name': '来源',
                'get_choices': [('', "--------")] + list(constants.Customer_Source.STATUS),
            },
            {
                'id': 'course',
                'verbose_name': '咨询课程',
                'get_choices': [('', "--------")] + list(constants.Course_Constants.STATUS),
            },
            {
                'id': 'class_type',
                'verbose_name': '咨询课程',
                'get_choices': [('', "--------")] + list(constants.Class_Type_Constants.STATUS),
            },
            {
                'id': 'status',
                'verbose_name': '状态',
                'get_choices': [('', "--------")] + list(constants.Customer_Status.STATUS),
            },
            {
                'id': 'consultant',
                'verbose_name': '课程顾问',
                'get_choices': [('', "--------")] + [
                    (i.id, i.name)
                    for i in models.UserProfile.objects.all()
                    ],
            },
        ]
        # 列表头
        context['list_display'] = [
            {'verbose_name': 'QQ名称', 'id': 'qq_name'},
            {'verbose_name': '学号', 'id': 'stu_id'},
            {'verbose_name': '姓名', 'id': 'name'},
            {'verbose_name': '咨询课程', 'id': 'course'},
            {'verbose_name': '班级类型', 'id': 'class_type'},
            {'verbose_name': '客户状态', 'id': 'colored_status'},
            {'verbose_name': '已报班级', 'id': 'get_enrolled_course'},
            {'verbose_name': 'qq号', 'id': 'qq'},
            {'verbose_name': '客户咨询内容详情', 'id': 'customer_note'},
            {'verbose_name': '课程顾问', 'id': 'consultant'},
            {'verbose_name': '咨询日期', 'id': 'date'},
            {'verbose_name': '操作', 'id': 'id'},
        ]

        context['list_display_buttons'] = [
            {
                'name': u'详情',
                'icon': 'fa-sticky-note',
                'type': 'get_info',
                'action': 'get_info'
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
                'type': 'get_adds',
                'action': 'adds'
            },
        ]
        # 配置搜索框
        # 不开启 写 False
        context['search'] = {
            'name': 'qq__contains'
        }
        return context

    def get_context_Pk(self, context, pk, **kwargs):
        self.template_name = 'crm/common_detail.html'  # 页面地址
        context['page_action'] = 'get_describe_list'

        context['page_title'] = '客户信息'

        return context

    def get_context_add(self, context, **kwargs):
        self.template_name = 'crm/common_add.html'  # 页面地址
        context['page_action'] = 'get_describe_list'

        context['page_title'] = '客户信息'

        return context

def main():
    pass


if __name__ == '__main__':
    main()
