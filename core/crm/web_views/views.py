# _*_coding:utf-8_*_
import json

import core.crm.web_models.survery_handle
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

import core.crm.web_models.models
import core.crm.web_views.class_grade
import core.crm.web_views.forms

from core.adminlte.web_views.views import CommonPageViewMixin, TemplateView
import logging

logger = logging.getLogger(__name__)
from .. import admin


# Create your views here.




def index(request):
    return render(request, 'crm/index.html')


def survery(request, survery_id):
    if request.method == "GET":
        try:
            survery_obj = core.crm.web_models.models.Survery.objects.get(id=survery_id)
            return render(request, "crm/survery.html", {"survery_obj": survery_obj})
        except ObjectDoesNotExist:
            return HttpResponse(u"问卷不存在")
    elif request.method == "POST":
        print dir(request)
        client_id = request.COOKIES.get("csrftoken")
        # print request.environ 8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM
        # print request.environ 8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM

        form_data = json.loads(request.POST.get("data"))
        survery_handler = core.crm.web_models.survery_handle.Survery(client_id, survery_id, form_data)
        if survery_handler.is_valid():
            survery_handler.save()

        else:
            print(survery_handler.errors)
        # print(form_data)

        return HttpResponse(json.dumps(survery_handler.errors))


@login_required
def survery_report(request, survery_id):
    try:
        survery_obj = core.crm.web_models.models.Survery.objects.get(id=survery_id)
        # class_obj..se

    except ObjectDoesNotExist as e:
        return HttpResponse("Survery doesn't exist!")

    return render(request, 'crm/survery_report.html', {'survery_obj': survery_obj})


@login_required
def survery_chart_report(request, survery_id):
    try:
        survery_obj = core.crm.web_models.models.Survery.objects.get(id=survery_id)
        # survery_obj.surveryrecord_set.select_related()
        chart_data = core.crm.web_models.survery_handle.generate_chart_data(survery_obj)

        return HttpResponse(json.dumps(chart_data))
    except ObjectDoesNotExist as e:
        return HttpResponse("Survery doesn't exist!")


@login_required
def view_class_grade(request, class_id):
    try:
        class_obj = core.crm.web_models.models.ClassList.objects.get(id=class_id)
        # class_obj..se

    except ObjectDoesNotExist as e:
        return HttpResponse("Class doesn't exist!")
    grade_gen_obj = core.crm.web_views.class_grade.ClassGrade(class_obj)
    grades = grade_gen_obj.fetch_grades()
    if grade_gen_obj.errors:
        html = u"<h4 style='color:red'>需为以下学员生成上课纪录后才能进行班级成绩查询,如果此学生之前没上课,生成上课纪录时选择缺勤即可</h4><ul>"
        for err in grade_gen_obj.errors:
            html += "<li>%s</li>" % err
        else:
            html += u'''</ul> 点击 <a href="/crm/stu_lack_check_records?class_id=%s&stu_ids=%s">为以上学员批量补齐上课纪录</a>''' % (
                class_obj.id, ",".join(grade_gen_obj.stu_lack_check_record))
        return HttpResponse(html)
    return render(request, 'crm/class_grade.html', {'class_obj': class_obj,
                                                    'class_grade_list': grades,
                                                    'study_record_model': core.crm.web_models.models.StudyRecord
                                                    })


def grade_check(request):
    if request.method == 'GET':
        return render(request, 'crm/grade_check.html')
    elif request.method == 'POST':
        errors = []
        stu_obj = None
        search_str = request.POST.get("search_str")
        if search_str:
            search_str = search_str.strip()
            if len(search_str) == 0:
                errors.append(u"查询不能为空!")
            else:

                try:
                    stu_obj = core.crm.web_models.models.Customer.objects.get(qq=search_str)
                except ObjectDoesNotExist as e:
                    errors.append(u"QQ号不存在!")
        else:
            errors.append(u"查询字段不能为空!")
        return render(request, 'crm/grade_check.html', {'errors': errors,
                                                        'stu_obj': stu_obj,
                                                        'study_record_model': core.crm.web_models.models.StudyRecord})


@login_required
def stu_lack_check_records(request):
    '''use this function to make up missing course check in records for some late enrolled students'''
    class_id = request.GET.get("class_id")
    stu_ids = request.GET.get('stu_ids')
    if stu_ids:
        stu_ids = stu_ids.split(',')
    class_obj = core.crm.web_models.models.ClassList.objects.get(id=class_id)
    for stu_id in stu_ids:

        for course_day in class_obj.courserecord_set.select_related():
            try:
                core.crm.web_models.models.StudyRecord.objects.get_or_create(course_record_id=course_day.id,
                                                                             student_id=stu_id,
                                                                             record='noshow',

                                                                             )
            except Exception as e:
                pass
    return HttpResponseRedirect("/crm/grade/%s" % class_id)


def scholarship(request):
    return render(request, 'crm/scholarship.html')


def compliant(request):
    if request.method == "GET":
        compliant_form = core.crm.web_views.forms.CompliantForm()
        return render(request, "crm/compliant.html", {"compliant_form": compliant_form})
    elif request.method == "POST":
        compliant_form = core.crm.web_views.forms.CompliantForm(request.POST)
        if compliant_form.is_valid():
            compliant_form.save()
            return HttpResponse(
                u"<h3 style='color:red'>感谢您的建议,我们将尽快认真处理,如果您留下了联系方式,我们会在2个工作日内与你联系并告诉您所提交的投诉或建议的处理进度或结果...have a nice day!</h3><a href='/'>返回首页</a>")
        return render(request, "crm/compliant.html", {"compliant_form": compliant_form})


def stu_faq(request):
    return render(request, "crm/stu_faq.html")


class Customer_View(CommonPageViewMixin, TemplateView):
    Page_Admin = admin.CustomerAdmin
    Page_Models = admin.models.Customer

    def get_context_data(self, **kwargs):
        """
            get 请求返回结果
            """
        context = super(Customer_View, self).get_context_data(**kwargs)
        pk = self.request.GET.get('pk')
        add = self.request.GET.get('add')
        logger.info(u"pk_id:%s add:%s" % (pk, add))
        context['page_action_name'] = 'crm_customer'
        if pk is None:
            return self.get_context_data_list(context, **kwargs)
        else:
            return self.get_context_data_detail(pk, context, **kwargs)

    def get_context_data_detail(self, pk, context, **kwargs):

        self.template_name = 'crm/common_detail.html'  # 页面地址
        context['page_action'] = 'customer_info'

        context['page_title'] = 'Customer %s 详情' % self.Page_Models.objects.get(id=pk).name
        context['nid'] = pk
        context['list_display_buttons'] = [
            {'name': u'详情', 'type': 'logsdetail'},
        ]
        context['all_list_display_buttons'] = [
            {'name': u'刷新', 'type': 'search'},
        ]
        return context

    def get_my_list_display(self):
        list_display = []
        for i in self.Page_Admin.list_display:
            try:
                list_display.append((i, self.Page_Models._meta.get_field(i)))
            except:
                list_display.append(
                    (i, {'verbose_name': i})
                )
        return list_display

    def get_context_data_list(self, context, **kwargs):
        self.template_name = 'crm/common_list.html'
        context['page_action'] = 'get_customer_list'

        context['page_title'] = 'Customer 列表'
        context['list_filter'] = [
            self.Page_Models._meta.get_field(i)
            for i in self.Page_Admin.my_list_filter
            ]
        context['list_display'] = self.get_my_list_display
        context['list_display_buttons'] = [
            {'name': u'详情', 'type': 'detail'},
        ]
        context['all_list_display_buttons'] = [
            {'name': u'刷新', 'type': 'search'},
        ]
        return context
