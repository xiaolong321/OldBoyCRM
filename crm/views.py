#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import models
import json
import survery_handle
import class_grade
import forms
from django.db.models import Sum,Count

# Create your views here.




def index(request):
    return  render(request,'crm/index.html')

def survery(request,survery_id):
    if request.method == "GET":
        try:
            survery_obj = models.Survery.objects.get(id=survery_id)
            return render(request,"crm/survery.html",{"survery_obj":survery_obj})
        except ObjectDoesNotExist:
            return HttpResponse(u"问卷不存在")
    elif request.method == "POST":
        print dir(request)
        client_id =  request.COOKIES.get("csrftoken")
        #print request.environ 8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM
        #print request.environ 8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM

        form_data = json.loads(request.POST.get("data"))
        survery_handler = survery_handle.Survery(client_id,survery_id,form_data)
        if survery_handler.is_valid():
            survery_handler.save()

        else:
            print(survery_handler.errors)
        #print(form_data)

        return HttpResponse(json.dumps(survery_handler.errors))
@login_required
def survery_report(request,survery_id):
    try:
        survery_obj = models.Survery.objects.get(id=survery_id)
        #class_obj..se

    except ObjectDoesNotExist as e:
        return HttpResponse("Survery doesn't exist!")

    return render(request,'crm/survery_report.html',{'survery_obj':survery_obj})


@login_required
def survery_chart_report(request,survery_id):
    try:
        survery_obj = models.Survery.objects.get(id=survery_id)
        #survery_obj.surveryrecord_set.select_related()
        chart_data = survery_handle.generate_chart_data(survery_obj)

        return HttpResponse(json.dumps(chart_data))
    except ObjectDoesNotExist as e:
        return HttpResponse("Survery doesn't exist!")

@login_required
def view_class_grade(request,class_id):
    try:
        class_obj = models.ClassList.objects.get(id=class_id)
        #class_obj..se

    except ObjectDoesNotExist as e:
        return HttpResponse("Class doesn't exist!")
    grade_gen_obj = class_grade.ClassGrade(class_obj)
    grades = grade_gen_obj.fetch_grades()
    if grade_gen_obj.errors:
        html = u"<h4 style='color:red'>需为以下学员生成上课纪录后才能进行班级成绩查询,如果此学生之前没上课,生成上课纪录时选择缺勤即可</h4><ul>"
        for err in grade_gen_obj.errors:
            html += "<li>%s</li>" % err
        else:
            html += u'''</ul> 点击 <a href="/crm/stu_lack_check_records?class_id=%s&stu_ids=%s">为以上学员批量补齐上课纪录</a>''' % (class_obj.id, ",".join(grade_gen_obj.stu_lack_check_record) )
        return HttpResponse(html)
    return render(request,'crm/class_grade.html',{'class_obj':class_obj,
                                                  'class_grade_list':grades,
                                                  'study_record_model':models.StudyRecord
                                                  })


def grade_check(request):

    if request.method == 'GET':
        return  render(request,'crm/grade_check.html')
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
                    stu_obj = models.Customer.objects.get(qq=search_str)
                except ObjectDoesNotExist as e:
                    errors.append(u"QQ号不存在!")
        else:
            errors.append(u"查询字段不能为空!")
        return  render(request,'crm/grade_check.html',{'errors':errors,
                                                       'stu_obj':stu_obj,
                                                       'study_record_model':models.StudyRecord})



@login_required
def stu_lack_check_records(request):
    '''use this function to make up missing course check in records for some late enrolled students'''
    class_id = request.GET.get("class_id")
    stu_ids = request.GET.get('stu_ids')
    if stu_ids:
        stu_ids = stu_ids.split(',')
    class_obj = models.ClassList.objects.get(id=class_id)
    for stu_id in stu_ids:

        for course_day in class_obj.courserecord_set.select_related():
            try:
                models.StudyRecord.objects.get_or_create(course_record_id=course_day.id,
                                                         student_id= stu_id,
                                                         record = 'noshow',

                                                         )
            except Exception as e:
                pass
    return HttpResponseRedirect("/crm/grade/%s" % class_id)

def scholarship(request):

    return render(request,'crm/scholarship.html')


def compliant(request):

    if request.method == "GET":
        compliant_form = forms.CompliantForm()
        return render(request,"crm/compliant.html",{"compliant_form":compliant_form})
    elif request.method == "POST":
        compliant_form = forms.CompliantForm(request.POST)
        if compliant_form.is_valid():
            compliant_form.save()
            return HttpResponse(u"<h3 style='color:red'>感谢您的建议,我们将尽快认真处理,如果您留下了联系方式,我们会在2个工作日内与你联系并告诉您所提交的投诉或建议的处理进度或结果...have a nice day!</h3><a href='/'>返回首页</a>")
        return render(request,"crm/compliant.html",{"compliant_form":compliant_form})
def stu_faq(request):

    return render(request,"crm/stu_faq.html")


@login_required
def get_grade_chart(request,stu_id):
    stu_obj = models.Customer.objects.get(id=stu_id)
    #print('---stuid', stu_obj)
    class_grade_dic = {}
    for class_obj in stu_obj.class_list.select_related(): #loop all the courses this student enrolled in
        class_grade_dic[class_obj.id] = {'record_count':[]}

        for stu in class_obj.customer_set.select_related():
            stu_scores = stu.studyrecord_set.select_related().values('course_record__course_id','student__name','student_id').annotate(score_count=Sum('score'))
            for score_dic in stu_scores: #有可能有多个课程
                if score_dic['course_record__course_id']  == class_obj.id:
                    class_grade_dic[class_obj.id]['record_count'].append([
                        score_dic['student_id'] ,
                        score_dic['student__name'] ,
                        score_dic['score_count'] ,
                    ])
                    '''class_grade_dic[class_obj.id]['record_count'].append({
                        'value':score_dic['score_count'],
                        'name':score_dic['student__name']
                    })'''
        #加上排名
        class_grade_dic[class_obj.id]['record_count'] = sorted(class_grade_dic[class_obj.id]['record_count'],key=lambda x:x[2])
    print(class_grade_dic)
    return HttpResponse(json.dumps(class_grade_dic))