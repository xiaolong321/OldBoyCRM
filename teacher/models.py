#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from django.db import models
from crm.models import *
from django.utils.html import format_html
from OldboyCRM import settings
import os
from crm.myauth import UserProfile

# Create your models here.


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
