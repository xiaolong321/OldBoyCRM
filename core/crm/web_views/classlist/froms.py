#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
from django import forms
from ...web_models.constants import *
from ...admin import models
class classlistadd(forms.ModelForm):
    class Meta:
        model = models.ClassList
        fields = [
            'course',
            'semester',
            'start_date',
            'graduate_date',
            'teachers'
        ]

    # course = forms.CharField(
    #     label='课程名称:',
    #     error_messages={
    #         'required': u'请选择项目'
    #     },
    #     widget=forms.Select(
    #         attrs={
    #             'class': "form-control"
    #         }))
    # semester = forms.CharField(
    #     label='学期:',
    #     required=False,
    #     error_messages={'required': u'备注不能为空'},
    #     widget=forms.TextInput(attrs={'class': "form-control"})
    # )
    # start_date = forms.DateField(
    #     label='开班日期:',
    #     required=False,
    #     error_messages={'required': u'备注不能为空'},
    # )
    # graduate_date = forms.DateField(
    #     label='结业日期:',
    #     required=False,
    #     error_messages={'required': u'备注不能为空'},
    # )
    # teachers = forms.CharField(
    #     label='讲师:',
    #     error_messages={
    #         'required': u'请选择项目'
    #     },
    #     widget=forms.Select(
    #         attrs={
    #             'class': "form-control"
    #         })
    # )
#
    # def __init__(self, *args, **kwargs):
    #     super(classlistadd, self).__init__(*args, **kwargs)
    #     self.fields['course'].widget.choices = Course_Constants.STATUS
    #     self.fields['teachers'].widget.choices = (
    #         (1, 'alex')
    #     )
