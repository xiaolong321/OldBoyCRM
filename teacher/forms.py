# !/usr/bin/env python
# -*- coding:utf-8 -*-


from django.forms import ModelForm,Textarea,BooleanField
from django import forms
from crm.models import CourseRecord



class CourserecordForm(ModelForm,):

    class Meta:
        model = CourseRecord
        exclude = ()

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {'class': 'form-control',
                        'placeholder': field.help_text,
                        }
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)