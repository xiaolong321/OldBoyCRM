# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = [
    url(r'403.html', TemplateView.as_view(template_name='adminlte/403.html'),
        name='http403'),
]
