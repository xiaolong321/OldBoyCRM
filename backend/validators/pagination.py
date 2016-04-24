# coding=utf-8
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.compat import OrderedDict

__author__ = 'lyhapple'


class CommonPageNumberPagination(PageNumberPagination):
    """
    简单的分页 模型
    """
    def get_paginated_response(self, data):
        """
        分页相应方法
        :param data:
        :return:
        """
        count = self.page.paginator.count  # 获取总条数
        total_page = self.page.paginator.num_pages  # 获取当前页面
        return Response(OrderedDict([  # 构造返回函数.
            ('per_page', self.page_size),  # 每页数量.
            ('current_page', self.page.number),  # 当前页数
            ('total_page', total_page),  # 总页数
            ('count', count),  # 总条数
            ('next', self.get_next_link()),  # 下一页连接地址
            ('previous', self.get_previous_link()),  # 上一页连接地址
            ('results', data),  # 当前数据
        ]))
