#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.db import models
from crm.models import *
from django.utils.html import format_html
from OldboyCRM import settings
import os
from crm.myauth import UserProfile

# Create your models here.
class teacher(models.Model):

    class Meta:
        verbose_name = "老师列表"
        verbose_name_plural = "老师列表"

        permissions = (
            ('teacher_view_teacher_dashboard', '访问 老师 主页'),
            ('teacher_view_classlist', '访问 教授课程 页面'),
            ('teacher_view_courselist', '访问 课程节次 页面'),
            ('teacher_view_courserecord', '访问 课程节次详细 页面'),
            ('teacher_edit_courserecord', '编辑 课程节次详细 页面'),
            ('teacher_view_createcourse', '访问 创建课程节次 页面'),
            ('teacher_edit_createcourse', '编辑 创建课程节次 页面'),
        )
