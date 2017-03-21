#!/usr/bin/env python3
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
        permissions = (
            ('teacher_view_teacher_dashboard', '访问 老师 主页'),
            ('teacher_view_classlist', '访问 教授课程 页面'),
            ('teacher_view_courselist', '访问 课程节次 页面'),
            ('teacher_edit_courselist', '下载出勤记录 页面'),
            ('teacher_view_courserecord', '访问 课程节次详细 页面'),
            ('teacher_edit_courserecord', '编辑 课程节次详细 页面'),
            ('teacher_view_createcourse', '访问 创建课程节次 页面'),
            ('teacher_edit_createcourse', '编辑 创建课程节次 页面'),
            ('teacher_view_editcourse', '访问 编辑课程节次 页面'),
            ('teacher_edit_editcourse', '编辑 编辑课程节次 页面'),
            ('teacher_view_studentinformation', '访问 学生信息 页面'),
            ('teacher_edit_studentinformation', '编辑学生信息 页面'),
            ('teacher_view_study_consult_record', '访问 创建学习跟踪记录 页面'),
            ('teacher_edit_study_consult_record', '编辑 创建学习跟踪记录 页面'),
            ('teacher_view_coursedetail', '访问 学习记录详细 页面'),
        )


class StudyConsultRecord(models.Model):
    enrollment = models.ForeignKey('crm.Enrollment', verbose_name='学生信息')
    status = models.CharField(max_length=64, verbose_name='跟进原因')
    note = models.TextField(u"跟进内容")
    consultant = models.ForeignKey(UserProfile, verbose_name=u"跟踪人")
    date = models.DateField(u"跟进日期", auto_now_add=True)

    def __str__(self):
        return u"{}-{}" .format(self.enrollment.customer.name, self.status)

    class Meta:
        verbose_name = u'学员学习跟踪记录'
        verbose_name_plural = u"客户学习跟踪记录"
