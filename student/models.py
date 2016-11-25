from django.db import models
from crm.models import *

class Stutest(models.Model):
    name=models.CharField('姓名',max_length=20)
    age = models.CharField('年龄',max_length=20)

class StuAccount(models.Model):
    stu_name = models.OneToOneField(Customer,verbose_name='关联对象')
    stu_pwd = models.CharField('密码',max_length=40)
    expiry_date = models.DateField(blank=True,null=True)

    class Meta:
        verbose_name='学员认证表'
        verbose_name_plural = '学员认证表'

    def __str__(self):

        return  '%s (%s)' % (self.stu_name.qq,self.stu_name.name)

