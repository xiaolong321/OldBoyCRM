#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import models
import json,os
import survery_handle
import class_grade
import forms
from django.db.models import Sum,Count
from OldboyCRM import settings
from django.http import FileResponse
from django.utils.encoding import smart_str
import zipfile,random

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


#@login_required
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
        #添加及格线
        class_course_records = class_obj.courserecord_set.select_related().filter(has_homework=True)
        qualifiy_benchmark = (class_course_records.count() * 100) *0.65
        class_grade_dic[class_obj.id]['record_count'].append([
            -1,u'及格线',qualifiy_benchmark
        ])
        print("---qualify benchmark ", qualifiy_benchmark)

        #加上排名
        class_grade_dic[class_obj.id]['record_count'] = sorted(class_grade_dic[class_obj.id]['record_count'],key=lambda x:x[2])
    print(class_grade_dic)
    return HttpResponse(json.dumps(class_grade_dic))


def stu_enrollment(request):
    qq = request.GET.get('stu_qq')
    if request.method == "GET":
        if qq:
            try:
                enroll_obj = models.Enrollment.objects.get(customer__qq=qq,contract_agreed=False)
                customer_form = forms.CustomerForm(instance=enroll_obj.customer)
                enroll_form = forms.EnrollmentForm(instance=enroll_obj)
                return render(request,'crm/enroll_page.html',{'enroll_form':enroll_form,'customer_form':customer_form})
            except ObjectDoesNotExist as e:
                try:
                    enroll_obj = models.Enrollment.objects.get(customer__qq=qq)
                    if enroll_obj.contract_approved:
                        return HttpResponse("培训协议已生成,请到首页查询")
                except ObjectDoesNotExist as e:
                    return HttpResponse("报名表不存在")
                return HttpResponse("报名表正在审核中")

        else:
            return HttpResponse("请求错误,qq号未提供")
    else:
        if qq:
            try:
                enroll_obj = models.Enrollment.objects.get(customer__qq=qq,contract_agreed=False)
                upload_path = '%s/%s'%(settings.ENROLL_DATA_DIR,enroll_obj.customer.id)
            except ObjectDoesNotExist as e:
                return HttpResponse(u"未查到相应的报名表,也有可能是报名表正在审批中,请到首页查询")
            if request.FILES:
                if not os.path.exists(upload_path):
                    os.mkdir(upload_path)
                abs_filepath = "%s/%s" %(upload_path,request.FILES['file'].name)

                if len(os.listdir(upload_path)) < 4:
                    if request.FILES['file'].size < 5*1024*1024: #5MB
                        with open(abs_filepath,'wb') as f:
                            for chunk in request.FILES['file'].chunks():
                                f.write(chunk)
                        return HttpResponse('upload success')

                    else:
                        return HttpResponseForbidden('文件大小不能超过5MB')
                else:
                    return HttpResponseForbidden('最多上传不超过4个文件')
            else:
                enroll_form = forms.EnrollmentForm(request.POST,instance=enroll_obj)
                customer_form = forms.CustomerForm(request.POST,instance=enroll_obj.customer)
                if enroll_form.is_valid() and customer_form.is_valid():

                    #check whether file has uploaded or not
                    file_sources_upload_path = "%s/%s" %(settings.ENROLL_DATA_DIR,enroll_obj.customer.id)
                    file_uploaded = False
                    try:
                        if len(os.listdir(file_sources_upload_path)) >0:#has file in this dir
                            new_check_password = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890~!@#$%^&*',8))
                            enroll_form.save()
                            customer_form.save()
                            enroll_obj.check_passwd = new_check_password
                            enroll_obj.save()
                            file_uploaded = True
                    except OSError as e:
                        file_uploaded = False
                    if file_uploaded == False:
                        return render(request,'crm/enroll_page.html',{'enroll_form':enroll_form,
                                                                  'customer_form':customer_form,
                                                                  'file_upload_err':u'证件资料未上传!'    })
                    return HttpResponse('''<h4>报名表已提交,待审批通过后可到<a href="http://crm.oldboyedu.com/crm/training_contract/">培训协议查询</a>
                                                查询生成的培训合同,查询密码为 <span style='color:red'>%s</span> </h4>''' %new_check_password)
                else:

                    uploaded_files = []
                    if  os.path.exists(upload_path):
                        uploaded_files = os.listdir(upload_path)
                    return render(request,'crm/enroll_page.html',{'enroll_form':enroll_form,
                                                                  'customer_form':customer_form,
                                                                  'uploaded_files':uploaded_files})


def training_contract(request):
    errors = ''
    if request.method == "POST":
        qq_num = request.POST.get('qq_num')
        check_passwd = request.POST.get('check_passwd')
        if not qq_num or not check_passwd:
            errors = "不合法的qq号或查询密码!"
        if not errors:
            try:
                enroll_obj = models.Enrollment.objects.get(customer__qq=qq_num,check_passwd=check_passwd)
                return render(request,"crm/contract_check.html",{'enroll_obj':enroll_obj})

            except ObjectDoesNotExist as e:
                errors =  "不合法的qq号或查询密码!"
    return render(request,"crm/contract_check.html",{'errors':errors})


@login_required
def file_download(request):

    customer_file_path = request.GET.get('file_path')
    if customer_file_path:

        filename = '%s.zip'  %customer_file_path.split('/')[-1] #compress filename

        file_list = os.listdir(customer_file_path)
        print('filelist',file_list)
        zipfile_obj = zipfile.ZipFile("%s/%s" %(settings.ENROLL_DATA_DIR,filename) ,'w',zipfile.ZIP_DEFLATED)
        for f_name in file_list:
            zipfile_obj.write("%s/%s" % (customer_file_path,f_name),f_name)
        zipfile_obj.close()

        response = FileResponse(open('%s.zip' % customer_file_path, 'rb'))
        #response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        response['X-Sendfile'] = smart_str(customer_file_path)
        #response['Content-Length'] = os.stat(file_path).st_size
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.

        return response

    else:
        raise  KeyError
