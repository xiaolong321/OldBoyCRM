# _*_coding:utf-8_*_
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from core.adminlte.web_views.views import CommonPageViewMixin, TemplateView

import logging

logger = logging.getLogger(__name__)
from ... import admin


class Views(CommonPageViewMixin, TemplateView):
    Page_Admin = admin.SurveryAdmin
    Page_Models = admin.models.Survery
    page_action_name = 'crm_survery'
    def get_context_data(self, **kwargs):
        """get 请求返回结果 """
        context = super(Views, self).get_context_data(**kwargs)
        pk = self.request.GET.get('pk')
        add = self.request.GET.get('add')
        logger.info(u"pk_id:%s add:%s" % (pk, add))
        context['page_action_name'] = self.page_action_name
        if add:
            return self.get_context_data_detail(pk, context, **kwargs)
        if pk is None:
            return self.get_context_data_list(context, **kwargs)
        else:
            return self.get_context_data_detail(pk, context, **kwargs)

    def get_context_data_detail(self, pk, context, **kwargs):

        self.template_name = 'crm/common_detail.html'  # 页面地址
        context['page_action'] = 'get_common_detail'

        context['page_title'] = u'%s %s 详情' % (
            self.Page_Models._meta.verbose_name,
            self.Page_Models.objects.get(id=pk).name
        )

        context['nid'] = pk
        context['list_display_buttons'] = [
            {'name': u'详情', 'type': 'logsdetail'},
        ]
        context['all_list_display_buttons'] = [
            {'name': u'刷新', 'type': 'search'},
        ]
        return context

    def get_my_list_display(self):
        list_display = []
        for i in self.Page_Admin.list_display:
            try:
                list_display.append((i, self.Page_Models._meta.get_field(i)))
            except:
                try:
                    list_display.append(
                        (i, {'verbose_name': getattr(self.Page_Models, i).short_description})
                    )
                except:
                    pass
        return list_display

    def get_my_list_filter(self):
        list_filters = []
        try:
            list_filter = self.Page_Admin.my_list_filter
        except:
            list_filter = self.Page_Admin.list_filter
        for i in list_filter:
            try:
                list_filters.append((i, getattr(self.Page_Models,i)._meta))
            except Exception as e:
                pass
        return list_filters

    def get_context_data_list(self, context, **kwargs):
        self.template_name = 'crm/common_list.html'
        context['page_action'] = 'get_common_list'

        context['page_title'] = self.Page_Models._meta.verbose_name
        context['list_filter'] = self.get_my_list_filter()
        context['list_display'] = self.get_my_list_display()
        context['list_display_buttons'] = [
            {'name': u'详情', 'type': 'detail'},
        ]
        context['all_list_display_buttons'] = [
            {'name': u'刷新', 'type': 'search'},
        ]
        return context
