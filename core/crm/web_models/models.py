# _*_coding:utf8_*_

from django.db import models

# Create your models here.
from django.utils.html import format_html

from core.adminlte.web_models.myauth import UserProfile
from .constants import *


class Customer(models.Model):
    qq = models.CharField(
        max_length=64,
        unique=True,
        help_text=u'QQ号必须唯一'
    )
    qq_name = models.CharField(
        u'QQ名称',
        max_length=64,
        blank=True,
        null=True
    )
    name = models.CharField(
        u'姓名',
        max_length=32,
        blank=True,
        null=True
    )
    phone = models.BigIntegerField(
        u'手机号',
        blank=True,
        null=True
    )
    stu_id = models.CharField(
        u"学号",
        blank=True,
        null=True,
        max_length=64
    )

    source = models.CharField(
        u'客户来源',
        max_length=64,
        choices=Customer_Source.STATUS,
        default=Customer_Source.QQ
    )
    referral_from = models.ForeignKey(
        'self',
        verbose_name=u"转介绍自学员",
        help_text=u"若此客户是转介绍自内部学员,请在此处选择内部学员姓名",
        blank=True,
        null=True,
        related_name="internal_referral"
    )

    course = models.CharField(
        u"咨询课程",
        max_length=64,
        choices=Course_Constants.STATUS
    )
    class_type = models.CharField(
        u"班级类型",
        max_length=64,
        choices=Class_Type_Constants.STATUS
    )

    customer_note = models.TextField(
        u"客户咨询内容详情",
        help_text=u"客户咨询的大概情况,客户个人信息备注等..."
    )
    # id_num = models.CharField(
    #   u'身份证号',
    #   max_length=64,
    #   blank=True,
    #   null=True
    # )

    status = models.CharField(
        u"状态",
        choices=Customer_Status.STATUS,
        max_length=64,
        default=Customer_Status.unregistered,
        help_text=u"选择客户此时的状态"
    )
    consultant = models.ForeignKey(
        UserProfile,
        verbose_name=u"课程顾问"
    )
    date = models.DateField(
        u"咨询日期",
        auto_now_add=True
    )

    class_list = models.ManyToManyField(
        'ClassList',
        verbose_name=u"已报班级",
        blank=True
    )

    def colored_status(self):
        if self.status == "signed":
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">已报名</span>')
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:gray;color:white">未报名</span>')
        elif self.status == "paid_in_full":
            format_td = format_html('<span style="padding:2px;background-color:orange;color:white">学费已交齐</span>')

        return format_td

    def get_enrolled_course(self):
        return " | ".join(["%s(%s)" % (i.get_course_display(), i.semester) for i in self.class_list.select_related()])

    get_enrolled_course.short_description = u'已报班级'
    colored_status.admin_order_field = u'客户状态'
    colored_status.short_description = u'客户状态'

    def __unicode__(self):
        return u"QQ:%s -- Stu:%s -- Name:%s" % (self.qq, self.stu_id, self.name)

    class Meta:
        verbose_name = u'客户信息表'
        verbose_name_plural = u"客户信息表"


class ConsultRecord(models.Model):
    customer = models.ForeignKey(
        Customer,
        verbose_name=u"所咨询客户"
    )
    note = models.TextField(
        u"跟进内容..."
    )
    status = models.IntegerField(
        u"状态",
        choices=ConsultRecord_Status.STATUS,
        help_text=u"选择客户此时的状态"
    )

    consultant = models.ForeignKey(
        UserProfile,
        verbose_name=u"跟踪人"
    )
    date = models.DateField(
        u"跟进日期",
        auto_now_add=True
    )

    def __unicode__(self):
        return u"%s, %s" % (self.customer, self.status)

    class Meta:
        verbose_name = u'客户咨询跟进记录'
        verbose_name_plural = u"客户咨询跟进记录"


class PaymentRecord(models.Model):
    customer = models.ForeignKey(
        Customer,
        verbose_name=u"客户"
    )
    course = models.CharField(
        u"课程名",
        choices=Course_Constants.STATUS,
        max_length=64
    )
    class_type = models.CharField(
        u"班级类型",
        choices=Class_Type_Constants.STATUS,
        max_length=64
    )

    pay_type = models.CharField(
        u"费用类型",
        choices=PaymentRecord_pay_type.STATUS,
        max_length=64,
        default=PaymentRecord_pay_type.deposit
    )
    paid_fee = models.IntegerField(
        u"费用数额",
        default=0
    )
    note = models.TextField(
        u"备注",
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        u"交款日期",
        auto_now_add=True
    )
    consultant = models.ForeignKey(
        UserProfile,
        verbose_name=u"负责老师",
        help_text=u"谁签的单就选谁"
    )

    def __unicode__(self):
        return u"%s, 类型:%s,数额:%s" % (
            self.customer,
            self.pay_type,
            self.paid_fee
        )

    class Meta:
        verbose_name = u'交款纪录'
        verbose_name_plural = u"交款纪录"


class ClassList(models.Model):
    course = models.CharField(
        u"课程名称",
        max_length=64,
        choices=Course_Constants.STATUS
    )
    semester = models.IntegerField(
        u"学期"
    )
    start_date = models.DateField(
        u"开班日期"
    )
    graduate_date = models.DateField(
        u"结业日期",
        blank=True,
        null=True
    )
    teachers = models.ManyToManyField(
        UserProfile,
        verbose_name=u"讲师"
    )

    def __unicode__(self):
        return u"%s(%s)" % (
            self.get_course_display(),
            self.semester
        )

    class Meta:
        verbose_name = u'班级列表'
        verbose_name_plural = u"班级列表"
        unique_together = (
            "course",
            "semester"
        )

    def get_student_num(self):
        return "%s" % self.customer_set.select_related().count()

    get_student_num.short_description = u'学员数量'


class CourseRecord(models.Model):
    course = models.ForeignKey(
        ClassList,
        verbose_name=u"班级(课程)"
    )
    day_num = models.IntegerField(
        u"节次",
        help_text=u"此处填写第几节课或第几天课程...,必须为数字"
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name=u"上课日期"
    )
    teacher = models.ForeignKey(
        UserProfile,
        verbose_name=u"讲师"
    )

    def __unicode__(self):
        return u"%s 第%s天" % (
            self.course,
            self.day_num
        )

    class Meta:
        verbose_name = u'上课纪录'
        verbose_name_plural = u"上课纪录"
        unique_together = (
            'course',
            'day_num'
        )

    def get_total_show_num(self):
        total_shows = self.studyrecord_set.select_related().filter(
            record="checked"
        ).count()
        return "<a href='../studyrecord/?course_record__id__exact=%s&record__exact=checked' >%s</a>" % (
            self.id,
            total_shows
        )

    def get_total_late_num(self):
        total_shows = self.studyrecord_set.select_related().filter(
            record="late"
        ).count()
        return "<a href='../studyrecord/?course_record__id__exact=%s&record__exact=late' >%s</a>" % (
            self.id,
            total_shows
        )

    def get_total_noshow_num(self):
        total_shows = self.studyrecord_set.select_related().filter(
            record="noshow"
        ).count()
        return "<a href='../studyrecord/?course_record__id__exact=%s&record__exact=noshow' >%s</a>" % (
            self.id,
            total_shows
        )

    def get_total_leave_early_num(self):
        total_shows = self.studyrecord_set.select_related().filter(record="leave_early").count()
        return "<a href='../studyrecord/?course_record__id__exact=%s&record__exact=leave_early' >%s</a>" % (
            self.id,
            total_shows
        )

    get_total_leave_early_num.allow_tags = True
    get_total_noshow_num.allow_tags = True
    get_total_late_num.allow_tags = True
    get_total_show_num.allow_tags = True
    get_total_show_num.short_description = u"出勤人数"
    get_total_noshow_num.short_description = u"缺勤人数"
    get_total_late_num.short_description = u"迟到人数"
    get_total_leave_early_num.short_description = u"早退人数"


class StudyRecord(models.Model):
    course_record = models.ForeignKey(
        CourseRecord,
        verbose_name=u"第几天课程"
    )
    student = models.ForeignKey(
        Customer,
        verbose_name=u"学员"
    )
    record = models.CharField(
        u"上课纪录",
        choices=StudyRecord_record.STATUS,
        default=StudyRecord_record.checked,
        max_length=64
    )
    score = models.IntegerField(
        u"本节成绩",
        choices=StudyRecord_score.STATUS,
        default=StudyRecord_score.N_A
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    note = models.CharField(
        u"备注",
        max_length=255,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u"%s,学员:%s,纪录:%s, 成绩:%s" % (
            self.course_record,
            self.student.name,
            self.record,
            self.get_score_display()
        )

    class Meta:
        verbose_name = u'学员学习纪录'
        verbose_name_plural = u"学员学习纪录"
        unique_together = (
            u'course_record',
            u'student'
        )

    def colored_record(self):
        color_dic = {
            u'checked': u"#5DFC70",
            u'late': u"#FFBF00",
            u'noshow': u"#B40404",
            u'leave_early': u"#FFFF00",
        }
        html_td = '<span style="padding:5px;background-color:%s;">%s</span>' % (
            color_dic[self.record],
            self.get_record_display()
        )
        return html_td

    def colored_score(self):
        html_td = '<span style="padding:5px;background-color:%s;">%s</span>' % (
            StudyRecord_score.get_color(
                code=self.score
            ),
            self.score
        )
        return html_td

    colored_score.allow_tags = True
    colored_record.allow_tags = True
    colored_score.short_description = u'成绩'
    colored_record.short_description = u'签到情况'


class SurveryItem(models.Model):
    name = models.CharField(
        u"调查问题",
        max_length=255,
        help_text=u"此处填写需要调查的问题...",
        unique=True
    )
    date = models.DateField(
        auto_now_add=True
    )
    anwser_type = models.CharField(
        u"问题类型",
        choices=SurveryItem_anwser_type.STATUS,
        default=SurveryItem_anwser_type.score,
        max_length=32
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'调查问卷问题列表'
        verbose_name_plural = u"调查问卷问题列表"


class Survery(models.Model):
    name = models.CharField(
        u"调查问卷名称",
        max_length=128,
        unique=True
    )
    questions = models.ManyToManyField(
        SurveryItem,
        verbose_name=u"选择要调查的问题列表"
    )
    by_class = models.ForeignKey(
        ClassList,
        verbose_name=u"问卷调查班级"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u"问卷创建日期"
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'调查问卷'
        verbose_name_plural = u"调查问卷"


class SurveryRecord(models.Model):
    survery = models.ForeignKey(
        Survery,
        verbose_name=u"问卷"
    )
    student_name = models.CharField(
        u"学员姓名",
        help_text=u"若是匿名问卷,姓名可不填写",
        blank=True,
        null=True,
        max_length=255
    )
    survery_item = models.ForeignKey(
        SurveryItem,
        verbose_name=u"调查项"
    )
    score = models.IntegerField(
        u"评分",
        help_text=u"打分为0至10,0为非常不满意,10为非常满意,请自行斟酌"
    )
    suggestion = models.TextField(
        u"建议",
        max_length=1024,
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=u"打分日期"
    )
    client_id = models.CharField(
        max_length=128,
        verbose_name=u"客户机id,会自动生成,莫改",
        default=".."
    )

    def __unicode__(self):
        return u"%s -- %s -- %s -- %s" % (
            self.survery,
            self.student_name,
            self.survery_item,
            self.score
        )

    class Meta:
        verbose_name = u'问卷记录'
        verbose_name_plural = u"问卷记录"


class Compliant(models.Model):
    compliant_type = models.CharField(
        u"选择类型",
        choices=Compliant_compliant_type.STATUS,
        max_length=32,
        default=Compliant_compliant_type.compliant
    )
    title = models.CharField(
        max_length=128,
        help_text=u"标题..."
    )
    content = models.TextField(
        max_length=1024,
        help_text=u"投诉或建议内容...."
    )
    name = models.CharField(
        u"姓名",
        help_text=u"不填则为匿名投诉\建议...",
        max_length=32
    )
    date = models.DateTimeField(
        u"创建日期",
        auto_now_add=True
    )
    status = models.CharField(
        u"状态",
        choices=Compliant_Status.STATUS,
        max_length=32,
        default=Compliant_Status.unread
    )
    comment = models.TextField(
        u"处理结果备注",
        help_text=u"处理方案,必填...",
        blank=True,
        null=True
    )
    dealing_time = models.DateTimeField(
        u"处理时间",
        blank=True,
        null=True
    )
    dealer = models.ForeignKey(
        UserProfile,
        verbose_name=u"处理人",
        blank=True,
        null=True
    )

    def __unicode__(self):
        return "%s --- %s" % (
            self.title,
            self.status
        )

    class Meta:
        verbose_name = u"学员投诉\建议"
        verbose_name_plural = u"学员投诉\建议"


class StudentFAQ(models.Model):
    title = models.CharField(
        u"问题",
        max_length=128
    )
    solution = models.TextField(
        u"答案"
    )
    author = models.ForeignKey(
        UserProfile,
        verbose_name=u"作者"
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = u"学员常见问题汇总"
        verbose_name_plural = u"学员常见问题汇总"
