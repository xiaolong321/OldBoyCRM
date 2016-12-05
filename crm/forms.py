#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from django.forms import ModelForm,Textarea,BooleanField
from django import forms
from crm.models import Compliant,Enrollment,Customer,ConsultRecord,PaymentRecord,CourseModule,ClassList


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
        

# 办理报名表
class EnroForm(ModelForm,forms.Form):
 
    class Meta:
        model = Enrollment
        exclude=('why_us','your_expectation','check_passwd','status')
    def __init__(self,*args,**kwargs):
        super(EnroForm,self).__init__(*args,**kwargs)
        self.fields['customer'].widget.attrs.update({'class':'form-control'})
        self.fields['course_grade'].widget.attrs.update({'class':'selectpicker'})
        self.fields['memo'].widget.attrs.update({'class':'form-control'})
        self.fields['school'].widget.attrs.update({'class':'selectpicker'})


#添加新用户表
class AddCustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude=('class_list','referral_from')

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {'class': 'form-control',
                        'placeholder':field.help_text,
                        }
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)




#增加新的跟进记录表
class AddConsultRecordForm(ModelForm):
    class Meta:
        model = ConsultRecord
        exclude =()
        error_messages={'note':{'required':'必填'},
                        'status':{'required':'必填'}}
    def __init__(self,*args,**kwargs):
        super(AddConsultRecordForm,self).__init__(*args,**kwargs)
        self.fields['customer'].widget.attrs.update({'class':'form-control'})
        self.fields['note'].widget.attrs.update({'class':'form-control','placeholder':'请先用几个字简要概括跟进情况，然后再详述。'})
        self.fields['status'].widget.attrs.update({'class':'form-icon form-control '})
        self.fields['consultant'].widget.attrs.update({'class':'form-control form-icon'})

class PaymentrecordForm(ModelForm):
    class Meta:
        model=PaymentRecord
        exclude=('course','class_type')

    def __init__(self,*args,**kwargs):
        super(PaymentrecordForm,self).__init__(*args,**kwargs)
        self.fields['customer'].widget.attrs.update({'class':'form-icon form-control'})
        self.fields['classlist'].widget.attrs.update({'class':'form-control'})
        self.fields['pay_type'].widget.attrs.update({'class':'form-control'})
        self.fields['paid_fee'].widget.attrs.update({'class':'form-control'})
        self.fields['note'].widget.attrs.update({'class':'form-control '})
        self.fields['consultant'].widget.attrs.update({'class':'form-control'})




class LoginForm(forms.Form):
    username = forms.EmailField(max_length=255,error_messages={'required':'用户名不能为空','invalid':'必须是邮箱格式'},widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),max_length=255,error_messages={'required':'密码不能为空'})
        

class CoursemoduleForm(ModelForm):
    class Meta:
        model=CourseModule
        exclude=('classlist',)

    def __init__(self, *args, **kwargs):
        super(CoursemoduleForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-icon form-control'})
        self.fields['memo'].widget.attrs.update({'class': 'form-control'})
        # self.fields['classlist'].widget.attrs.update({'class': 'form-control'})

class ClasslistForm(ModelForm):
    class Meta:
        model=ClassList
        exclude=()

    def __init__(self, *args, **kwargs):
        super(ClasslistForm, self).__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.update({'class': 'form-icon form-control'})
        self.fields['semester'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control','placeholder':'必须是  1990/01/01 格式'})
        self.fields['graduate_date'].widget.attrs.update({'class': 'form-control','placeholder':'必须是  1990/01/01 格式'})
        self.fields['contract'].widget.attrs.update({'class': 'form-control'})
        self.fields['teachers'].widget.attrs.update({'class': 'form-control'})
        self.fields['memo'].widget.attrs.update({'class': 'form-control','placeholder':'建议写明该课程为何种课程，何种形式。如：Linux架构师-面授（周末）班', })


