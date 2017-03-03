# !/usr/bin/env python3
# -*- coding:utf-8 -*-


from django.forms import ModelForm,Textarea,BooleanField
from django import forms
from crm.models import CourseRecord
from teacher.models import StudyConsultRecord



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


class AddStudyConsultRecordForm(ModelForm):

    class Meta:
        model = StudyConsultRecord
        exclude =()
        error_messages={'note':{'required':'必填'},
                        'status':{'required':'必填'}}
    def __init__(self,*args,**kwargs):
        super(AddStudyConsultRecordForm,self).__init__(*args,**kwargs)
        self.fields['enrollment'].widget.attrs.update({'class':'form-control'})
        self.fields['note'].widget.attrs.update({'class':'form-control','placeholder':'请先用几个字简要概括跟进情况，然后再详述。'})
        self.fields['status'].widget.attrs.update({'class':'form-icon form-control '})
        self.fields['consultant'].widget.attrs.update({'class':'form-control form-icon'})