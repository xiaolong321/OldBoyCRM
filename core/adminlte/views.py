# coding=utf-8
from django.contrib.auth import views

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView, TemplateView, DetailView
from core.adminlte import constants
from core.adminlte.models import SystemConfig


__author__ = 'lyhapple'


def get_app_model_name(kwargs):
    app_name = kwargs.get('app_name').lower()
    model_name = kwargs.get('model_name').lower()
    return app_name, model_name


def get_model_content_type(app_name, model_name):
    return ContentType.objects.get(app_label=app_name, model=model_name)


def get_system_config_value(key_name):
    try:
        return SystemConfig.objects.get(name=key_name).value
    except:
        return u'未找到 %s 系统配置项' % key_name


class CommonPageViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CommonPageViewMixin, self).get_context_data(**kwargs)
        default_dashboard_title = constants.DEFAULT_DASHBOARD_TITLE
        if hasattr(self, 'model'):
            page_title = self.model._meta.verbose_name
        else:
            page_title = default_dashboard_title

        common_dict = {
            'page_menus': [],
            'default_dashboard_title': default_dashboard_title,
            'page_title': page_title,
            'page_model': getattr(self, 'model', ''),
            'page_app_name': getattr(self, 'app_name', ''),
            'page_model_name': getattr(self, 'model_name', ''),
            'page_system_name': get_system_config_value('system_name'),
            'page_system_subhead': get_system_config_value('system_subhead')
        }
        context.update(common_dict)
        return context


class IndexView(CommonPageViewMixin, TemplateView):
    template_name = "adminlte/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return context


class ChangePasswordView(CommonPageViewMixin, TemplateView):
    def post(self, request, **kwargs):
        self.request = request
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        context['page_title'] = u'修改密码'
        template_response = views.password_change(
            self.request,
            template_name='adminlte/change-password.html',
            extra_context=context
        )
        return template_response


class ChangePasswordDoneView(CommonPageViewMixin, TemplateView):
    template_name = 'adminlte/change-password-done.html'
