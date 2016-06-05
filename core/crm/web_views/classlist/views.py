#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging

logger = logging.getLogger(__name__)
from core.adminlte.web_views.views import CommonPageViewMixin, TemplateView

class Views(CommonPageViewMixin, TemplateView):

    def get_context_data(self, **kwargs):
        """
        get 请求返回结果
        """
        context = super(Views, self).get_context_data(**kwargs)
        # 调用的 api 的 action_name
        # 没有生效 .去 js里面改.action_name 即可
        context['page_action_name'] = 'classlist'
        return self.get_context_data_list(context, **kwargs)

    def get_context_data_list(self, context, **kwargs):
        self.template_name = 'crm/common_list.html'  # 页面地址
        context['page_action'] = 'get_describe_list'

        context['page_title'] = '用户管理'
        # 自定义 类搜索
        # 这里可以直接从后端获取相关的搜索主键
        context['list_filter'] = [
            {
                'id': 'teachers',
                'verbose_name': '讲师',
                'get_choices': (
                    ('', "----------"),
                    ('1', "admin")
                ),
            }
        ]
        # 列表头
        context['list_display'] = [
            {'verbose_name': '课程名称', 'id': 'course'},
            {'verbose_name': '学期', 'id': 'semester'},
            {'verbose_name': '开班日期', 'id': 'start_date'},
            {'verbose_name': '结业日期', 'id': 'graduate_date'},
            {'verbose_name': '学员数量', 'id': 'student_num'},
            {'verbose_name': '讲师', 'id': 'teachers', 'type': 'Dialog'},
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
        ]
        # 配置搜索框
        # 不开启 写 False
        context['search'] = {
            'name': 'course'
        }
        return context


def main():
    pass


if __name__ == '__main__':
    main()
