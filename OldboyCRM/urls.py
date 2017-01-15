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
from  crm import urls as crm_urls
from crm import views as crm_views
from teacher import urls as teacher_urls
from student import urls as stu_urls
from OldboyCRM.settings import ENROLL_DATA_DIR


urlpatterns = [
    url(r'^stu/',include(stu_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crm/', include(crm_urls)),
    url(r'^teacher/', include(teacher_urls)),
    url(r'^$', crm_views.index ),
    url(r'^login/$', crm_views.login_url, name='login_url'),
]
