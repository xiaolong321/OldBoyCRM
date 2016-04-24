# _*_coding:utf-8_*_
"""OldboyCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from core.adminlte.web_views.views import IndexView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login_required(IndexView.as_view()), name='index'),
    url(r'^auth/', include("core.adminlte.urls",
                           namespace="registration")),
]

urlpatterns += [
]
if settings.DEBUG: #如果 开启 DEBUG 模式.会默认加载相关的目录信息
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)