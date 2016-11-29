#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.conf.urls import include, url
from teacher import views


urlpatterns = [
    url(r'^$',views.dashboard, name='teacher_dashboard'),  # 教师基页
    url(r'^classlist',views.classlist, name='classlist'),
    url(r'^courselist/(?P<class_id>\d+)',views.courselist, name='courselist'),
    url(r'^courserecord/(?P<course_id>\d+)',views.courserecord, name='courserecord'),
    url(r'^createcourse/(?P<class_id>\d+)',views.createcourse, name='createcourse'),
]
