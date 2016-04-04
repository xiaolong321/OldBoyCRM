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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from core.adminlte.views import IndexView, ChangePasswordView, \
    ChangePasswordDoneView



urlpatterns = [
    url('^page/change-password/$', ChangePasswordView.as_view(),
        name='change_password'),
    url('^page/change-password-done/$', ChangePasswordDoneView.as_view(),
        name='password_change_done'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', login_required(IndexView.as_view()), name='index'),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
]

# ===================== 自定义url映射 开始====================================
# 自定义url必须放在通用url的前面，将通用url覆盖掉
# Page url
urlpatterns += [
    url(r'^crm/', include('core.crm.urls',
                                      namespace='crms')),
]
# API url
urlpatterns += [
    #url(r'^api/v1/messageset', include('core.messageset.urls_api',
    #                                   namespace='messageset_api')),
    # url(r'^api/v1/organization', include('organization.urls',
    # namespace='organization_api')),
]

# ===================== 自定义url映射 结束 ==================================

# 通用URL映射，必须放在最后
urlpatterns += [
    # 通用页面URL映射，必须放在最后
    url(r'^page', include('core.adminlte.urls', namespace='adminlte')),
]


