#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import models
import json
import survery_handle
import class_grade
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
