# _*_coding:utf-8_*_
from django.contrib import admin

# Register your models here.

from core.crm.web_models import models


from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse


class ConsultRecordInline(admin.TabularInline):
    model = models.ConsultRecord


class PaymentRecordInline(admin.TabularInline):
    model = models.PaymentRecord


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ('qq', 'phone')
    raw_id_fields = ('referral_from',)
    filter_horizontal = ('class_list',)
    list_filter = ('source', 'course', 'class_type', 'status', 'date', 'consultant')
    my_list_filter = ('source', 'course', 'class_type', 'status', 'consultant')
    my_fieldsets = (
        (u'基础信息', {'no_input': ['qq'], 'fields': ('qq', 'qq_name', 'name', 'phone', 'stu_id')}),
    )
    inlines = [ConsultRecordInline, PaymentRecordInline]
    list_display = (
        'qq_name', 'stu_id', 'name', 'course', 'class_type',
            'colored_status', 'get_enrolled_course', 'qq', 'customer_note',
        'consultant', 'date','id', )
    # list_editable = ('status',)
    # def has_delete_permission(self, request, obj=None):
    #    return False
    add_list_dicsplay = ()
    actions = []

    def get_actions(self, request):
        actions = super(CustomerAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ConsultRecordAdmin(admin.ModelAdmin):
    raw_id_fields = ('customer',)
    list_display = ('customer', 'note', 'status', 'consultant', 'date')
    search_fields = ('customer__qq',)
    list_filter = ('status', 'consultant', 'date')

    def get_actions(self, request):
        actions = super(ConsultRecordAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class PaymentRecordAdmin(admin.ModelAdmin):
    raw_id_fields = ('customer',)

    list_display = ('customer', 'course', "class_type", "pay_type", "paid_fee", 'consultant', "note", "date", "id")
    search_fields = ('customer__qq',)
    list_filter = ('course', 'pay_type', 'class_type', 'consultant', 'date')

    def get_actions(self, request):
        actions = super(PaymentRecordAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CustomerInline(admin.TabularInline):
    model = models.Customer.class_list.through
    # fields = ('class_type',)
    # fields = ('class_type',)


class ClassListAdmin(admin.ModelAdmin):
    list_display = ("course", 'semester', "start_date", "graduate_date", "get_student_num")
    inlines = (CustomerInline,)
    actions = ['view_grade', ]

    def view_grade(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        if len(selected) > 1:
            return HttpResponse(u"只能同时查看一个班级的成绩情况,请确保只选一个班级再试!")
        return HttpResponseRedirect("/crm/grade/%s/" % selected[0])

    def get_actions(self, request):
        actions = super(ClassListAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    view_grade.short_description = u"查看成绩"


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ('course', 'day_num', 'date', 'teacher',
                    "get_total_show_num",
                    "get_total_noshow_num",
                    "get_total_late_num",
                    "get_total_leave_early_num",
                    'id'
                    )
    list_filter = ('course', 'day_num', 'teacher')

    actions = ['initialize_student_list']

    def initialize_student_list(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        # print(ct.pk,selected)
        if len(selected) > 1:
            return HttpResponse(u"只能同时初化一个班级的上课纪录,请确保只选一个班级再试!")
        class_num = models.CourseRecord.objects.get(id=selected[0])
        stu_list = class_num.course.customer_set.select_related()
        for stu in stu_list:
            models.StudyRecord.objects.get_or_create(course_record_id=selected[0],
                                                     student=stu,
                                                     )

        # return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/admin/crm/studyrecord/?course_record__id__exact=%s" % (selected[0]))

    initialize_student_list.short_description = u"初始化本节课学员出勤纪录"

    def get_actions(self, request):
        actions = super(CourseRecordAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class StudyRecordAdmin(admin.ModelAdmin):
    list_display = (
    'course_record', 'get_stu_name', 'get_stu_id', 'record', 'colored_record', 'colored_score', 'score', 'date', 'note', 'id')
    list_filter = ("course_record__course__course", "course_record", "score", "record")
    search_fields = ('student__name', 'student__stu_id')
    list_editable = ("score", "record", "note")
    actions = ["set_to_late", "set_to_noshow", "set_to_leave_early", "set_to_checked"]

    def set_to_late(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        models.StudyRecord.objects.filter(id__in=selected).update(record="late")

    def set_to_noshow(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        models.StudyRecord.objects.filter(id__in=selected).update(record="noshow")

    def set_to_leave_early(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        models.StudyRecord.objects.filter(id__in=selected).update(record="leave_early")

    def set_to_checked(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        models.StudyRecord.objects.filter(id__in=selected).update(record="checked")

    set_to_checked.short_description = u"设置所选学员为--已签到"
    set_to_leave_early.short_description = u"设置所选学员为--早退"
    set_to_noshow.short_description = u"设置所选学员为--缺勤"
    set_to_late.short_description = u"设置所选学员为--迟到"

    def get_actions(self, request):
        actions = super(StudyRecordAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_stu_id(self, obj):
        return obj.student.stu_id

    get_stu_id.admin_order_field = u'student__stu_id'  # Allows column order sorting
    get_stu_id.short_description = u'学号'  # Renames column head

    def get_stu_name(self, obj):
        return obj.student.name

    get_stu_name.admin_order_field = u'student__name'  # Allows column order sorting
    get_stu_name.short_description = u'姓名'  # Renames column head


class SurveryAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)
    actions = ['check_survery_report', ]

    def check_survery_report(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        # ct = ContentType.objects.get_for_model(queryset.model)
        if len(selected) > 1:
            return HttpResponse(u"只能同时查看一个问卷的统计报告,请确保只选一个问卷再试!")

        # return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
        return HttpResponseRedirect("/crm/survery/report/%s/" % (selected[0]))

    check_survery_report.short_description = u"查看问卷报告"


class SurveryRecordAdmin(admin.ModelAdmin):
    # filter_horizontal = ('questions',)
    list_display = ['survery', 'survery_item', 'score', 'suggestion', 'date']
    list_filter = ['survery_item', 'survery']

    def get_actions(self, request):
        actions = super(SurveryRecordAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_model_perms(self, request):
        """
        Returns a dict of all perms for this model. This dict has the keys
        ``add``, ``change``, and ``delete`` mapping to the True/False for each
        of those actions.
        """
        model_perms = super(SurveryRecordAdmin, self).get_model_perms(request)
        print model_perms
        if 'delete' in model_perms:
            model_perms['delete'] = False
        return model_perms

class CompliantAdmin(admin.ModelAdmin):
    list_display = ('compliant_type', 'title', 'content', 'name', 'date', 'dealing_time', 'status', 'comment')
    list_filter = ('compliant_type', 'status', 'date')


class StudentFAQAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'id')

class SurveryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'anwser_type', 'id')

admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.ConsultRecord, ConsultRecordAdmin)
admin.site.register(models.PaymentRecord, PaymentRecordAdmin)
admin.site.register(models.ClassList, ClassListAdmin)
admin.site.register(models.CourseRecord, CourseRecordAdmin)
admin.site.register(models.StudyRecord, StudyRecordAdmin)
admin.site.register(models.SurveryRecord, SurveryRecordAdmin)
admin.site.register(models.Survery, SurveryAdmin)
admin.site.register(models.SurveryItem)
admin.site.register(models.Compliant, CompliantAdmin)
admin.site.register(models.StudentFAQ, StudentFAQAdmin)
