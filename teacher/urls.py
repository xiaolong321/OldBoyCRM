#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from django.conf.urls import include, url
from teacher import views


urlpatterns = [
    url(r'^$',views.dashboard, name='teacher_dashboard'),  # 教师基页
    url(r'^login',views.my_login, name='teacher_my_login'),  # 教师登录页
    url(r'^logout',views.my_logout, name='teacher_my_logout'),
    url(r'^classlist',views.classlist, name='classlist'),
    url(r'^courselist/(?P<class_id>\d+)', views.courselist, name='courselist'),
    url(r'^courserecord/(?P<course_id>\d+)/(?P<student_id>\d+)', views.courserecord, name='courserecord'),
    url(r'^createcourse/(?P<class_id>\d+)', views.createcourse, name='createcourse'),
    url(r'^studentinformation/$', views.studentinformation, name='studentinformation'),
    url(r'^study_consult_record/(?P<enrollment_id>\d+)/$', views.study_consult_record, name='study_consult_record'),
]
