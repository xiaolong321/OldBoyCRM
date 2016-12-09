#coding:utf-8

import hashlib
from django.forms import ModelForm,Textarea,BooleanField
from django import forms
from student.models import *

def hashstr(inputstr):
    import hashlib
    inputstr=inputstr.encode()
    m = hashlib.md5()
    m.update(inputstr)
    resu = m.hexdigest()
    return resu

class StulogForm(forms.Form):
    stu_name=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    stu_pwd= forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))


class StudyrecordForm(ModelForm):
    class Meta:
        model= StudyRecord
        fields=('homework','stu_memo')
    def __init__(self,*args,**kwargs):
        super(StudyrecordForm,self).__init__(*args,**kwargs)
        self.fields['homework'].widget.attrs.update({'class':'form-control'})
        self.fields['stu_memo'].widget.attrs.update({'class':'form-control','placeholder':'非必填且仅限备注此次提交'})


class  ChangepwdForm(forms.Form):
    oldpwd  = forms.CharField(required=True,error_messages={'required':'请输入原密码'},
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'原密码'}))
    newpwd1 = forms.CharField(required=True,error_messages={'required':'请输入新密码'},
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'新密码'}))
    newpwd2 = forms.CharField(required=True,error_messages={'required':'请再次输入新密码'},
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'确认密码'}))
    def clean(self):
        cleaned_date = super(ChangepwdForm, self).clean()
        newpwd1 = cleaned_date['newpwd1']
        hash_newpwd1 = hashstr(newpwd1)
        cleaned_date['newpwd1']=hash_newpwd1
        newpwd2 = cleaned_date['newpwd2']
        hash_newpwd2 = hashstr(newpwd2)
        cleaned_date['newpwd2']=hash_newpwd2
        oldpwd = cleaned_date['oldpwd']
        hash_oldpwd = hashstr(oldpwd)
        cleaned_date['oldpwd']=hash_oldpwd
        return cleaned_date


class ReferralForm(ModelForm):
    class Meta:
        model = Referral
        exclude = ('referralfrom',)
        error_messages = {
            'qq':{
            'unique':'该同学已经存在'
            }
        }

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {
                'class': 'form-control',
                'placeholder': field.help_text,
            }
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)
