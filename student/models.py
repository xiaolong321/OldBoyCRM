from django.db import models
from crm.models import *

class StuAccount(models.Model):
    stu_name = models.OneToOneField(Customer,verbose_name='关联对象')
    stu_pwd = models.CharField('密码',max_length=40)
    expiry_date = models.DateField(blank=True,null=True)

    class Meta:
        verbose_name='学员认证表'
        verbose_name_plural = '学员认证表'

    def __str__(self):

        return  '%s (%s)' % (self.stu_name.qq,self.stu_name.name)


class Referral(models.Model):
    referralfrom = models.ForeignKey(StuAccount,verbose_name='推荐人')
    qq = models.CharField(u'QQ',max_length=64,unique=True,)
    phone = models.BigIntegerField(u'手机号')
    name = models.CharField(u'姓名',max_length=32)
    comment = models.TextField(u"备注",help_text=u"推荐的同学的大体状况，比如学习意愿，文化水平等等")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"课程顾问")
    referral_date = models.DateTimeField(auto_now_add=True,auto_created=True,verbose_name="推荐日期")

    class Meta:
        verbose_name='学员推荐表'
        verbose_name_plural = '学员推荐表'

    def __str__(self):

        return  '%s (%s)' % (self.qq,self.name)