#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from django.forms import ModelForm,Textarea,BooleanField
from django import forms
from models import Compliant,Enrollment,Customer


class CompliantForm(ModelForm):
    class Meta:
        model = Compliant
        fields = ('title','compliant_type','content','name')

        widgets = {
            'content': Textarea(attrs={'cols': 100, 'rows': 10,'name':'content','class':'form-control','placeholder':u"描述需达到15字以上..."}),
        }

    def __init__(self, *args, **kwargs):
        super(CompliantForm, self).__init__(*args, **kwargs)
        #slect_css='''height:26px;min-width:155px; border: solid 1px #E5E5E5;background: -webkit-gradient(linear, left top, left 25, from(#FFFFFF), color-stop(4%, #EEEEEE), to(#FFFFFF));'''
        #self.fields['description'].widget.attrs.update({'class' : 'form-control','placeholder':'task description','rows':3})
        self.fields['title'].widget.attrs.update({'class' : 'form-control input-lg','name':'title'})
        self.fields['compliant_type'].widget.attrs.update({'class' : 'form-control'})
        self.fields['name'].widget.attrs.update({'class' : 'form-control input-sm','placeholder':u"请留下您的姓名,若想匿名则可不填..."})



class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('qq','name','phone','email','sex',
                  'birthday','id_num','work_status',
                  'company','salary','consultant')

    def __new__(cls,*args,**kwargs):
        #super(CustomerForm, self).__new__(*args, **kwargs)
        #self.fields['customer_note'].widget.attrs['class'] = 'form-control'
        disabled_fields = ['qq','consultant']
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {'class': 'form-control',
                        'placeholder':field.help_text,
                        }
            if field_name in disabled_fields:
                attr_dic['disabled'] = True
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)

class EnrollmentForm(ModelForm):
    contract_agreed = BooleanField(required=True,label=u"我已认真阅读完培训协议并同意全部协议内容")
    class Meta:
        model = Enrollment
        fields = ('why_us','your_expectation','course_grade','contract_agreed')

    def __new__(cls,*args,**kwargs):
        #super(EnrollmentForm, self).__init__(*args, **kwargs)
        #self.fields['customer_note'].widget.attrs['class'] = 'form-control'

        disabled_fields = ['course_graded',]
        class_exempt = ['contract_agreed',]
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {'class': 'form-control',
                        'placeholder':field.help_text,
                        }
            if field_name in class_exempt:
                attr_dic['class']= ''
            if field_name in disabled_fields:
                attr_dic['disabled'] = True
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)
