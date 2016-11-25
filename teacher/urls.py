#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.conf.urls import include, url
from teacher import views


urlpatterns = [
    url(r'^$',views.dashboard),  # 教师基页
    url(r'^classlist',views.classlist),
    url(r'^rollcall/(?P<class_id>\d+)',views.rollcall),
    url(r'^courselist/(?P<class_id>\d+)',views.courselist),
    url(r'^courserecord/(?P<course_id>\d+)',views.courserecord),
    url(r'^createcourse/(?P<class_id>\d+)',views.createcourse),
]