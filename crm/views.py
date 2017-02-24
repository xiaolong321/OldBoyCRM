# _*_coding:utf-8_*_

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, resolve_url
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from crm import models
import json, os, random, zipfile, datetime
from crm import survery_handle
from crm import class_grade
from crm import forms
from django.db.models import Sum, Count, Q
from OldboyCRM import settings
from django.http import FileResponse
from django.utils.encoding import smart_str
from django.contrib.auth import login, logout, authenticate
from crm.html_helper import PageInfo, Page
from crm.myauth import UserProfile
from django.contrib.auth.models import Group
from student.models import StuAccount
from crm.permissions import check_permission
from student.forms import Referral
from common.message import message
import string
import random
import os
import shutil
from OldboyCRM.settings import ENROLL_DATA_DIR, CONSULT_DATA_DIR, HOMEWORK_DATA_DIR, ATTENDANCE_DATA_DIR, consultant_list
from django.utils.http import urlquote
from teacher.views import my_login as teacher_my_login


def hashstr(inputstr):
    import hashlib
    inputstr = inputstr.encode()
    m = hashlib.md5()
    m.update(inputstr)
    resu = m.hexdigest()
    return resu


def makePassword(minlength=5, maxlength=12):
    length = random.randint(minlength, maxlength)
    letters = string.ascii_letters + string.digits
    return ''.join([random.choice(letters) for _ in range(length)])


def index(request):
    return render(request, 'crm/index.html')


def survery(request, survery_id):
    if request.method == "GET":
        try:
            survery_obj = models.Survery.objects.get(id=survery_id)
            return render(request, "crm/survery.html", {"survery_obj": survery_obj})
        except ObjectDoesNotExist:
            return HttpResponse(u"问卷不存在")
    elif request.method == "POST":
        client_id = request.COOKIES.get("csrftoken")
        form_data = json.loads(request.POST.get("data"))
        survery_handler = survery_handle.Survery(client_id, survery_id, form_data)
        if survery_handler.is_valid():
            survery_handler.save()
        else:
            pass
        return HttpResponse(json.dumps(survery_handler.errors))


@login_required
def survery_report(request, survery_id):
    try:
        survery_obj = models.Survery.objects.get(id=survery_id)
    except ObjectDoesNotExist as e:
        return HttpResponse("Survery doesn't exist!")
    return render(request, 'crm/survery_report.html', {'survery_obj': survery_obj})


@login_required
def survery_chart_report(request, survery_id):
    try:
        survery_obj = models.Survery.objects.get(id=survery_id)
        # survery_obj.surveryrecord_set.select_related()
        chart_data = survery_handle.generate_chart_data(survery_obj)

        return HttpResponse(json.dumps(chart_data))
    except ObjectDoesNotExist as e:
        return HttpResponse("Survery doesn't exist!")


@login_required
def view_class_grade(request,class_id):
    try:
        class_obj = models.ClassList.objects.get(id=class_id)
        # class_obj..se
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

        #加上排名
        class_grade_dic[class_obj.id]['record_count'] = sorted(class_grade_dic[class_obj.id]['record_count'],key=lambda x:x[2])

    return HttpResponse(json.dumps(class_grade_dic))


def stu_enrollment(request):
    qq = request.GET.get('stu_qq')
    class_semester = request.GET.get('course_grade')
    the_class, the_semester = class_semester.split('_')
    try:
        class_obj = models.ClassList.objects.get(course=the_class, semester=the_semester)       # 限定班级
    except ObjectDoesNotExist:
        return HttpResponse('报名表不存在')
    if request.method == "GET":
        if qq:
            try:
                enroll_obj = models.Enrollment.objects.get(customer__qq=qq, course_grade=class_obj,
                                                           contract_agreed=False)
                customer_form = forms.CustomerForm(instance=enroll_obj.customer)
                enroll_form = forms.EnrollmentForm(instance=enroll_obj)
                return render(request, 'crm/enroll_page.html', {
                    'enroll_form': enroll_form,
                    'customer_form': customer_form})
            except ObjectDoesNotExist:
                try:
                    enroll_obj = models.Enrollment.objects.get(customer__qq=qq, course_grade=class_obj)
                    if enroll_obj.contract_approved:
                        return HttpResponse("培训协议已生成,请到首页查询")
                except ObjectDoesNotExist:
                    return HttpResponse("报名表不存在")
                return HttpResponse("报名表正在审核中")

        else:
            return HttpResponse("请求错误,qq号未提供")
    else:
        if qq:
            try:
                enroll_obj = models.Enrollment.objects.get(customer__qq=qq,
                                                           course_grade=class_obj, contract_agreed=False)
                upload_path = '%s/%s' % (settings.ENROLL_DATA_DIR, enroll_obj.customer.id)
            except ObjectDoesNotExist:
                return HttpResponse(u"未查到相应的报名表,也有可能是报名表正在审批中,请到首页查询")
            if request.FILES:
                if not os.path.exists(upload_path):
                    os.mkdir(upload_path)
                abs_filepath = "%s/%s" % (upload_path, request.FILES['file'].name)

                if len(os.listdir(upload_path)) < 4:
                    if request.FILES['file'].size < 5 * 1024 * 1024:        # 5MB
                        with open(abs_filepath, 'wb') as f:
                            for chunk in request.FILES['file'].chunks():
                                f.write(chunk)
                        return HttpResponse('upload success')

                    else:
                        return HttpResponseForbidden('文件大小不能超过5MB')
                else:
                    return HttpResponseForbidden('最多上传不超过4个文件')
            else:
                enroll_form = forms.EnrollmentForm(request.POST, instance=enroll_obj)
                customer_form = forms.CustomerForm(request.POST, instance=enroll_obj.customer)
                if enroll_form.is_valid() and customer_form.is_valid():

                    # check whether file has uploaded or not
                    file_sources_upload_path = "%s/%s" % (settings.ENROLL_DATA_DIR, enroll_obj.customer.id)
                    file_uploaded = False
                    try:
                        if len(os.listdir(file_sources_upload_path)) > 0:       # has file in this dir
                            new_check_password = ''.join(random.sample(
                                'zyxwvutsrqponmlkjihgfedcba1234567890~!@#$%^&*', 8))
                            enroll_form.save()
                            customer_form.save()
                            enroll_obj.check_passwd = new_check_password
                            enroll_obj.save()
                            file_uploaded = True
                    except OSError:
                        file_uploaded = False
                    if not file_uploaded:
                        return render(request, 'crm/enroll_page.html', {
                            'enroll_form': enroll_form,
                            'customer_form': customer_form,
                            'file_upload_err': u'证件资料未上传!'
                        })
                    return HttpResponse('''<h4>报名表已提交,待审批通过后可到
                    <a href="http://crm.oldboyedu.com/crm/training_contract/">培训协议查询</a>
                    查询生成的培训合同,查询密码为 <span style='color:red'>%s</span> </h4>''' % new_check_password)
                else:

                    uploaded_files = []
                    if os.path.exists(upload_path):
                        uploaded_files = os.listdir(upload_path)
                    return render(request, 'crm/enroll_page.html', {
                        'enroll_form': enroll_form,
                        'customer_form': customer_form,
                        'uploaded_files': uploaded_files
                    })


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
                errors = "不合法的qq号或查询密码!"
    return render(request,"crm/contract_check.html",{'errors':errors})


@login_required
def file_download(request):
    customer_file_path = request.GET.get('file_path')
    if customer_file_path:
        if customer_file_path.startswith(HOMEWORK_DATA_DIR):
            if len(customer_file_path.split(HOMEWORK_DATA_DIR)[-1].split('/')) == 4:
                filenames = (os.listdir(customer_file_path))
                for filename in filenames:
                    if filename.endswith('.zip'):
                        response = FileResponse(open('{}/{}'.format(customer_file_path, filename), 'rb'))
            elif len(customer_file_path.split(HOMEWORK_DATA_DIR)[-1].split('/')) == 3:
                filename = '%s.zip' % customer_file_path.split('/')[-1]
                # zipfile_path = "%s/%s" % (settings.HOMEWORK_DATA_DIR, customer_file_path.split('/')[-2])
                # zipfile_obj = zipfile.ZipFile("%s/%s" % (zipfile_path, filename), 'w', zipfile.ZIP_DEFLATED)
                # for dirpath, dirnames, filenames in os.walk(os.path.join(customer_file_path, 'all')):
                #     print(dirpath, dirnames, filenames)
                #     for file in filenames:
                #         zipfile_obj.write(os.path.join(dirpath,file),os.path.join(dirpath.split(os.path.join(customer_file_path,'all'))[-1],file))
                # zipfile_obj.close()
                response = FileResponse(open('%s.zip' % customer_file_path, 'rb'))

        else:
            customer_id = customer_file_path.split('/')[-1]
            customer = models.Customer.objects.filter(id=customer_id).first()
            filename = '%s.zip' % customer_id     # compress filename
            file_list = os.listdir(customer_file_path)
            if customer_file_path.startswith(ENROLL_DATA_DIR):
                zipfile_obj = zipfile.ZipFile("%s/%s" % (ENROLL_DATA_DIR, filename), 'w', zipfile.ZIP_DEFLATED)
            elif customer_file_path.startswith(CONSULT_DATA_DIR):
                zipfile_obj = zipfile.ZipFile("%s/%s/%s" % (CONSULT_DATA_DIR, customer.consultant.id, filename), 'w',
                                              zipfile.ZIP_DEFLATED)
            elif customer_file_path.startswith(ATTENDANCE_DATA_DIR):
                zipfile_obj = zipfile.ZipFile("%s/%s" % (ATTENDANCE_DATA_DIR, filename), 'w', zipfile.ZIP_DEFLATED)

            for f_name in file_list:
                zipfile_obj.write("%s/%s" % (customer_file_path, f_name), f_name)
            zipfile_obj.close()
            response = FileResponse(open('%s.zip' % customer_file_path, 'rb'))


        # response = FileResponse(open('%s.zip' % customer_file_path, 'rb'))
        # response = HttpResponse(content_type='application/force-download')
        #  mimetype is replaced by content_type for django 1.7
        response['Content-Disposition'] = 'attachment; filename=%s' % urlquote(filename)
        response['X-Sendfile'] = smart_str(customer_file_path)
        # response['Content-Type'] = 'application/force-download'
        response['Content_Type'] = 'application/octet-stream'
        # response['Content-Length'] = os.stat(customer_file_path).st_size
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.
        return response

    else:
        raise KeyError


@login_required
def dashboard(request):
    try:
        email = request.session['email']
        dict_org={'consultant__email':email,'status':'unregistered'}
    except KeyError as e:
        return HttpResponseRedirect(resolve_url('login_url'))
    cus=models.Customer.objects.filter(**dict_org)
    today= datetime.date.today()
    customers=[]
    result = {}
    for customer in cus:

        last_consult=customer.consultrecord_set.last()  #最后跟进记录

        if last_consult == None: #无跟进记录，以录入日期为准
            consultant_date = customer.date  #  录入日期
            midd_date = today - consultant_date  # 录入日期距 今天多久
            max_day = datetime.timedelta(days=90)  # 预期最大间隔时间
            min_day = datetime.timedelta(days=7)  # 预期最小间隔时间
            if min_day<=midd_date <= max_day:  # 最小间隔时间< 距今间隔 < 最大预期间隔
                customers.append(customer)   # 只截取距今天 7 天以外，90 天以内的跟进客户

        else:  #有跟进记录,以最后跟进记录日期为准
            last_date = customer.consultrecord_set.last().date  # 最后跟进日期
            midd_date = today - last_date  # 最后跟进日期距 今天多久
            max_day = datetime.timedelta(days=90)  # 预期最大间隔时间， 90 天
            min_day = datetime.timedelta(days=7)  # 预期最小间隔时间， 7 天
            if min_day<= midd_date <= max_day:   # 最小间隔时间< 距今间隔 < 最大预期间隔
                customers.append(customer)  #只截取最近15天内的跟进客户

    random.shuffle(customers) # 打乱客户随机顺序
    customers=customers[0:5]   # 只截取需跟进库的前5名
    count = len(customers)
    succe_track = {'customers':customers,'count':count}
    result.update(succe_track)

    # 以下为 销量排名图表 所需数据
    sales=[(i.email,i.name) for i in models.UserProfile.objects.filter(groups__name='sales').all()]
    # 销售用户列表 [('x.qq.com',张三），（'y@qq.com'，李四），（'z@qq.com',王五) ]
    sale_num={}  # 销售销量字典{姓名：[正跟进客户数，已签约客户数]}  ｛张三：[3,2],李四：[6,2]｝


    year= str(today)[0:4]
    month = str(today)[5:7]
    month_before='%s-%s-01'%(year,month)

    def count_all(x,y):
        count_list=[]
        if x + y == 0:
            count_list=[0,0]
        else:
            sum_all= (x+y)
            succ_cus = float('%.2f'%((y/(x+y))*100))
            count_list.extend([sum_all,succ_cus])
        return count_list

    for sale in sales:
        sale_track = models.Customer.objects.filter(status='unregistered',consultant__email=sale[0],date__gt=month_before,date__lt=today).count()  # 本月至今 正跟进客户数
        sale_signed=models.Customer.objects.exclude(status='unregistered').filter(consultant__email=sale[0],date__gt=month_before,date__lt=today).count()  # 本月至今 已签约客户数
        b =count_all(sale_track, sale_signed)
        a = [sale_track, sale_signed]
        a.extend(b)
        sale_num[sale[1]] =a

    b = True
    curr_url = request.path
    z = int(request.GET.get('o',1))


    sale_list = sorted(sale_num.items(),key=lambda x:x[1][z],reverse=b)[0:5]   # 筛选 签约客户量 前 N 名

    result['sale_list']=sale_list
    result['curr_url']=curr_url
    referrals = Referral.objects.filter(consultant=request.user)
    for referral in referrals:
        if models.Customer.objects.filter(qq=referral.qq):
            referral.flag = False
        else:
            referral.flag = True
    return render(request,'crm/dashboard.html',locals())


@login_required
def sale_table(request):
    if request.method == 'GET':
        sales =[i for i in models.UserProfile.objects.all() if not i.is_staff]
        sale_num = {}
        today = datetime.date.today()
        year = str(today)[0:4]
        month = str(today)[5:7]
        month_before = '%s-%s-01' % (year, month)
        for sale in sales:
            sale_track = models.Customer.objects.filter(status='unregistered',  consultant__email=sale.email,
				date__gt=month_before, date__lt=today).count()  # 本月至今 正跟进客户数
            sale_signed = models.Customer.objects.exclude(status='unregistered').filter(consultant__email=sale.email,
			date__gt=month_before,
			date__lt=today).count()  # 本月至今 已签约客户数
            sale_num[sale.name] = [sale_track, sale_signed,sale_track+sale_signed]

        sale_dict=json.dumps(sale_num)
        return HttpResponse(sale_dict)


@login_required
@check_permission
def tracking(request, page, *args, **kwargs):
    ord = []
    username = request.session['username']
    user = request.session['email']
    current_url = request.path
    GET = request.GET
    cus_sources = models.Customer.source_type  # 以客户来源
    cus_sources = map(lambda x: {'type': x[0], 'name': x[1]}, cus_sources)
    cus_sources = list(cus_sources)

    course = models.course_choices  # 以咨询课程
    course = map(lambda x: {'type': x[0], 'name': x[1]}, course)
    course = list(course)

    classes = models.class_type_choices  # 以班级类型
    classes = map(lambda x: {'type': x[0], 'name': x[1]}, classes)
    classes = list(classes)

    cus_status = (('unregistered',u"未报名"),)  # 客户状态
    cus_status = map(lambda x: {'type': x[0], 'name': x[1]}, cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.filter(email=user).values('email', 'name')  # 客户顾问
    staffs = map(lambda x: {'type': x['email'], 'name': x['name']}, staffs)
    staffs = list(staffs)

    filter_date = [{'type': 'today', 'name': '今天'}, {'type': 'sevendays', 'name': '七天以内'},
                   {'type': 'month', 'name': '近一个月'}, {'type': 'year', 'name': '今年'}]

    result = {
        'cus_sources': cus_sources,
        'course': course,
        'classes': classes,
        'cus_status': cus_status,
        'staffs': staffs,
        'current_url': current_url,
        'filter_date': filter_date,
    }

    now = datetime.datetime.now()
    sevenday = datetime.timedelta(days=7)
    today = now.strftime('%Y-%m-%d')  # 今天
    sevendaybef = (now - sevenday).strftime('%Y-%m-%d')  # 一周前
    amouth = datetime.timedelta(days=30)
    amouthbef = (now - amouth).strftime('%Y-%m-%d')  # 一个月前
    ayear = datetime.timedelta(days=365)
    ayearbef = (now - ayear).strftime('%Y-%m-%d')  # 一年前

    direct_org = { 'status': 'unregistered'}

    for item in kwargs.keys():

        if item == 'filter_date':  # 单独对日期进行处理
            if kwargs[item] == 'all':
                pass
            elif kwargs[item] == 'today':
                direct_org['date'] = today
            elif kwargs[item] == 'sevendays':
                direct_org['date__gte'] = sevendaybef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'month':
                direct_org['date__gte'] = amouthbef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'year':
                direct_org['date__gte'] = ayearbef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'range':
                start_time = GET.get('start_time')
                end_time = GET.get('end_time')
                direct_org['date__gte'] = start_time.replace('年', '-').replace('月', '-').replace('日', '')
                direct_org['date__lt'] = end_time.replace('年', '-').replace('月', '-').replace('日', '')
                result['start_time'] = start_time
                result['end_time'] = end_time

        else:
            if kwargs[item] != 'all':
                direct_org[item] = kwargs[item]

    if GET.get('qq'):
        qq_num_err = {}
        qq = GET['qq']
        try:
            qq = int(qq)
        except ValueError as e:
            qq_num_err={'qq_num_error': '只能输入QQ号'}

        direct_org.update({'qq': qq})

        con = Q()
        q1 = Q()
        q1.connector = 'AND'
        for key, value in direct_org.items():
            q1.children.append((key, value))
        q1.children.append(('consultant__email', user))
        q2 = Q()
        q2.connector = 'AND'
        for key, value in direct_org.items():
            if not key == 'status':
                q2.children.append((key, value))
        q2.children.append(('consultrecord__consultant__email', user))
        con.add(q1, 'OR')
        con.add(q2, 'OR')

        customers = models.Customer.objects.filter(con).distinct()
        count = customers.count()
        fil = {'customers': customers, 'count': count, }
        fil.update(qq_num_err)
        result.update(fil)

    else:
        try:
            page = int(page)
        except:
            page = 1

        values = request.COOKIES.values()
        if ('desc' not in values) and ('asc' not in values):
            ord = ['-last_consult_date']  # 如果没有选择排序，那么默认设置为按 id 排序
        else:
            ord = []

        for key in request.COOKIES.keys():
            if request.COOKIES[key] == 'asc' or request.COOKIES[key] == 'desc':
                if key != 'undefined':
                    if request.COOKIES[key] == 'desc':
                        ord.append('-' + key)
                    elif request.COOKIES[key] == 'asc':
                        ord.append(key)



        con = Q()
        q1 = Q()
        q1.connector = 'AND'
        for key, value in direct_org.items():
            q1.children.append((key, value))
        q1.children.append(('consultant__email', user))
        q2 = Q()
        q2.connector = 'AND'
        for key, value in direct_org.items():
            if not key == 'status':
                q2.children.append((key, value))
        q2.children.append(('consultrecord__consultant__email', user))
        con.add(q1, 'OR')
        con.add(q2, 'OR')
        count = models.Customer.objects.filter(con).distinct().count()
        pageObj = PageInfo(page, count, 50)
        customers = models.Customer.objects.filter(con).distinct().select_related().order_by(*ord)[pageObj.start:pageObj.end]
        fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])

        fil = {'customers': customers, 'count': count, 'fenye': fenye}

        result.update(fil)
    return render(request, 'crm/tracking.html', locals())


@login_required
@check_permission
def signed(request,page,*args,**kwargs):

    if request.method == 'POST':
        id=request.POST['id']
        cur_customer = models.Customer.objects.get(id=id)
        if request.POST['cus_sta'] == 'paid_in_full':
            cur_customer.status = 'paid_in_full'
            cur_customer.save()

    username = request.session['username']
    user = request.session['email']
    current_url = request.path
    GET = request.GET

    cus_sources = models.Customer.source_type  # 以客户来源
    cus_sources = map(lambda x: {'type': x[0], 'name': x[1]}, cus_sources)
    cus_sources = list(cus_sources)

    course = models.course_choices  # 以咨询课程
    course = map(lambda x: {'type': x[0], 'name': x[1]}, course)
    course = list(course)

    classes = models.class_type_choices  # 以班级类型
    classes = map(lambda x: {'type': x[0], 'name': x[1]}, classes)
    classes = list(classes)

    cus_status = (('signed', '已报名'), ('paid_in_full', '学费已交齐'))  # 客户状态
    cus_status = map(lambda x: {'type': x[0], 'name': x[1]}, cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.filter(email=user).values('email', 'name')  # 客户顾问
    staffs = map(lambda x: {'type': x['email'], 'name': x['name']}, staffs)
    staffs = list(staffs)

    filter_date = [{'type': 'today', 'name': '今天'}, {'type': 'sevendays', 'name': '七天以内'},
                   {'type': 'month', 'name': '近一个月'}, {'type': 'year', 'name': '今年'}]

    result = {
        'cus_sources': cus_sources,
        'course': course,
        'classes': classes,
        'cus_status': cus_status,
        'staffs': staffs,
        'current_url': current_url,
        'filter_date': filter_date,
    }

    now = datetime.datetime.now()
    sevenday = datetime.timedelta(days=7)
    today = now.strftime('%Y-%m-%d')  # 今天
    sevendaybef = (now - sevenday).strftime('%Y-%m-%d')  # 一周前
    amouth = datetime.timedelta(days=30)
    amouthbef = (now - amouth).strftime('%Y-%m-%d')  # 一个月前
    ayear = datetime.timedelta(days=365)
    ayearbef = (now - ayear).strftime('%Y-%m-%d')  # 一年前

    direct_org = {'consultant__email': user}
    exc = {'status': 'unregistered'}
    for item in kwargs.keys():

        if item == 'filter_date':  # 单独对日期进行处理
            if kwargs[item] == 'all':
                pass
            elif kwargs[item] == 'today':
                direct_org['date'] = today
            elif kwargs[item] == 'sevendays':
                direct_org['date__gte'] = sevendaybef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'month':
                direct_org['date__gte'] = amouthbef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'year':
                direct_org['date__gte'] = ayearbef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'range':
                start_time = GET.get('start_time')
                end_time = GET.get('end_time')
                direct_org['date__gte'] = start_time.replace('年', '-').replace('月', '-').replace('日', '')
                direct_org['date__lt'] = end_time.replace('年', '-').replace('月', '-').replace('日', '')
                result['start_time'] = start_time
                result['end_time'] = end_time

        else:
            if kwargs[item] != 'all':
                direct_org[item] = kwargs[item]

    if GET.get('qq'):
        qq_num_err = {}
        qq = GET['qq']
        try:
            qq = int(qq)
        except ValueError:
            qq_num_err = {'qq_num_error': '只能输入QQ号'}

        direct_org.update({'qq': qq})
        customers = models.Customer.objects.exclude(**exc).filter(**direct_org)
        count = models.Customer.objects.exclude(**exc).filter(**direct_org).count()
        fil = {'customers': customers, 'count': count,}
        fil.update(qq_num_err)
        result.update(fil)
    else:

        try:
            page = int(page)
        except:
            page = 1

        values = request.COOKIES.values()
        if ('desc' not in values) and ('asc' not in values):
            ord = ['-last_consult_date']  # 如果没有选择排序，那么默认设置为按 id 排序
        else:
            ord = []

        for key in request.COOKIES.keys():

            if request.COOKIES[key] == 'asc' or request.COOKIES[key] == 'desc':
                if key != 'undefined':
                    if request.COOKIES[key] == 'asc':
                        ord.append(key)
                    elif request.COOKIES[key] == 'desc':
                        ord.append('-' + key)

        count = models.Customer.objects.filter(**direct_org).exclude(**exc).count()
        pageObj = PageInfo(page, count, 50)
        customers = []
        customer_objs = models.Customer.objects.filter(**direct_org).exclude(**exc).select_related().order_by(*ord)[pageObj.start:pageObj.end]
        for customer_obj in customer_objs:
            payment_obj = models.PaymentRecord.objects.filter(customer=customer_obj).exclude(pay_type='refund')
            customers.append({'customer':customer_obj,'payments':payment_obj})

        fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])

        fil = {'customers': customers, 'count': count, 'fenye': fenye}

        result.update(fil)
    return render(request, 'crm/signed.html', result)


@login_required
@check_permission
def customers_library(request, page, *args, **kwargs):

    username = request.session['username']
    current_url = request.path
    GET = request.GET

    cus_sources = models.Customer.source_type       # 以客户来源
    cus_sources = map(lambda x: {'type': x[0], 'name': x[1]}, cus_sources)
    cus_sources = list(cus_sources)

    course = models.course_choices      # 以咨询课程
    course = map(lambda x: {'type': x[0], 'name': x[1]}, course)
    course = list(course)

    classes = models.class_type_choices     # 以班级类型
    classes = map(lambda x: {'type': x[0], 'name': x[1]}, classes)
    classes = list(classes)

    cus_status = models.Customer.status_choices     # 客户状态
    cus_status = map(lambda x: {'type': x[0], 'name': x[1]}, cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.filter(groups__name__in=consultant_list).values('email', 'name')  # 客户顾问
    staffs = map(lambda x: {'type': x['email'], 'name': x['name']}, staffs)
    staffs = list(staffs)

    filter_date = [{'type': 'today', 'name': '今天'}, {'type': 'sevendays', 'name': '七天以内'},
                   {'type': 'month', 'name': '近一个月'}, {'type': 'year', 'name': '今年'},]

    result = {
        'cus_sources': cus_sources,
        'course': course,
        'classes': classes,
        'cus_status': cus_status,
        'staffs': staffs,
        'current_url': current_url,
        'filter_date': filter_date,
    }

    now = datetime.datetime.now()
    sevenday = datetime.timedelta(days=7)
    today = now.strftime('%Y-%m-%d')  # 今天
    sevendaybef = (now - sevenday).strftime('%Y-%m-%d')  # 一周前
    amouth = datetime.timedelta(days=30)
    amouthbef = (now - amouth).strftime('%Y-%m-%d')  # 一个月前
    ayear = datetime.timedelta(days=365)
    ayearbef = (now - ayear).strftime('%Y-%m-%d')  # 一年前

    direct_org = {}
    for item in kwargs.keys():

        if item == 'filter_date':  # 单独对日期进行处理
            if kwargs[item] == 'all':
                pass
            elif kwargs[item] == 'today':
                direct_org['date'] = today
            elif kwargs[item] == 'sevendays':
                direct_org['date__gte'] = sevendaybef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'month':
                direct_org['date__gte'] = amouthbef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'year':
                direct_org['date__gte'] = ayearbef
                direct_org['date__lt'] = today
            elif kwargs[item] == 'range':
                start_time = GET.get('start_time')
                end_time = GET.get('end_time')
                direct_org['date__gte'] = start_time.replace('年','-').replace('月','-').replace('日','')
                direct_org['date__lt'] = end_time.replace('年','-').replace('月','-').replace('日','')
                result['start_time'] = start_time
                result['end_time'] = end_time


        else:
            if kwargs[item] != 'all':
                direct_org[item] = kwargs[item]

    if GET.get('qq'):
        qq_num_err = {}
        qq = GET['qq']
        try:
            qq = int(qq)
        except ValueError as e:
            qq_num_err = {'qq_num_error': '只能输入QQ号'}
        customers = models.Customer.objects.filter(qq=qq)
        count = models.Customer.objects.filter(qq=qq).count()
        fil = {'customers': customers, 'count': count, }
        fil.update(qq_num_err)

    else:
        try:
            page = int(page)
        except:
            page = 1

        count = models.Customer.objects.filter(**direct_org).count()

        try:
            page = int(page)
        except:
            page = 1
        pageObj = PageInfo(page, count, 50)

        values = request.COOKIES.values()
        if ('desc' not in values) and ('asc'not in values):
            ord = ['-last_consult_date']
            # customers= models.Customer.objects.filter(**direct_org).select_related().order_by('-consultrecord__date').distinct().groupby('consultrecord__date')[pageObj.start:pageObj.end]
            # # customers_obj= models.Customer.objects.filter(**direct_org).select_related().order_by('-consultrecord__date')
            # # customers = []
            # # flag = 0
            # # for customer in customers_obj:
            # #     if pageObj.start < flag < pageObj.end:
            # #         if customer not in customers:
            # #             customers.append(customer)
            # #     flag += 1
            # # customers = customers[pageObj.start:pageObj.end]
            # print(customers)
        else:
            ord = []

        for key in request.COOKIES.keys():

            if request.COOKIES[key] == 'asc' or request.COOKIES[key] == 'desc':
                if key != 'undefined':
                    if request.COOKIES[key] == 'asc':

                        ord.append(key)
                    elif request.COOKIES[key] == 'desc':

                        ord.append('-'+key)

        customers = models.Customer.objects.filter(**direct_org).select_related().order_by(*ord)[pageObj.start:pageObj.end]
        fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])

        fil = {'customers': customers, 'count': count, 'fenye': fenye}

    result.update(fil)
    return render(request, 'crm/customers_library.html', result)


@login_required
@check_permission
def addcustomer(request, referralfromid=None):
    curr_user = request.user
    username = request.user.email
    if request.method == 'POST':
        upload_path = '%s/%s/%s' % (settings.CONSULT_DATA_DIR, curr_user.id, 'temporary')
        if request.FILES:
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            abs_filepath = "%s/%s" % (upload_path, request.FILES['file'].name)
            if len(os.listdir(upload_path)) < 4:
                if request.FILES['file'].size < 5 * 1024 * 1024:  # 5MB
                    with open(abs_filepath, 'wb') as f:
                        for chunk in request.FILES['file'].chunks():
                            f.write(chunk)
                    return HttpResponse('upload success')
                else:
                    return HttpResponseForbidden('文件大小不能超过5MB')
            else:
                return HttpResponseForbidden('最多上传不超过4个文件')
        else:
            form = forms.AddCustomerForm(data=request.POST)
            if request.POST.get('source') == 'referral':
                from_student = models.Customer.objects.filter(qq=request.POST.get("referral_from")).first()
            else:
                from_student = None
            if form.is_valid():
                file_sources_upload_path = "%s/%s/%s" % (settings.CONSULT_DATA_DIR, curr_user.id, 'temporary')
                file_uploaded = False
                try:
                    if len(os.listdir(file_sources_upload_path)) > 0:  # has file in this dir
                        form.save()
                        from_student = models.Customer.objects.filter(qq=request.POST.get("referral_from")).first()
                        customer = models.Customer.objects.filter(qq=request.POST.get('qq')).first()
                        customer.referral_from = from_student
                        customer.save()
                        file_upload_path = "%s/%s/%s" % (settings.CONSULT_DATA_DIR, curr_user.id, customer.id)
                        if not os.path.exists(file_upload_path):
                            os.makedirs(file_upload_path)
                        root = file_sources_upload_path
                        a = os.walk(root)
                        for x in a:
                            if len(x[-1]) > 0:
                                for j in x[-1]:
                                    os.rename(x[0] + '/' + j, file_upload_path + '/' + j)
                        return HttpResponseRedirect(
                            resolve_url('tracking', 'all', 'all', 'all', 'all', 'all', 'all', '1'))
                except Exception:
                    file_uploaded = False
                if not file_uploaded:
                    return render(request, 'crm/addcustomer.html', {
                        'form': form,
                        'username': username,
                        'curr_user': curr_user,
                        'from_student': from_student,
                        'file_upload_err': u'咨询内容截图未上传!',
                    })
            else:
                uploaded_files = []
                if os.path.exists(upload_path):
                    uploaded_files = os.listdir(upload_path)
                return render(request, 'crm/addcustomer.html', {
                    'form': form,
                    'username': username,
                    'curr_user': curr_user,
                    'from_student': from_student,
                    'uploaded_files': uploaded_files,
                })
    if referralfromid:
        referralfrom = Referral.objects.filter(id=referralfromid).first()
        form = forms.AddCustomerForm(
            {
                'qq': referralfrom.qq,
                'phone': referralfrom.phone,
                'name': referralfrom.name,
                'source': 'referral',
                'customer_note': referralfrom.comment,
            })
        from_student = models.Customer.objects.filter(id=referralfrom.referralfrom.stu_name_id).first()
        return render(request, 'crm/addcustomer.html', {'form': form, 'username': username, 'curr_user': curr_user,
                                                        'from_student': from_student})
    else:
        form = forms.AddCustomerForm()
        return render(request, 'crm/addcustomer.html', {'form': form, 'username': username, 'curr_user': curr_user})


@login_required
def searchcustomer(request):
    if request.method == 'POST':
        from_student_qq = request.POST.get('student_qq')
        from_student = models.Customer.objects.filter(qq=from_student_qq)
        return HttpResponse(from_student)


@login_required
@check_permission
def cus_enroll(request, *args, **kwargs):
    username = request.session['username']            # 获取当前销售姓名
    id = kwargs['id']
    customer = models.Customer.objects.get(id=id)       # 获取当前用户
    classes = models.ClassList.objects.all()            # 获取所有的班级
    classes_list = customer.class_list.all()            # []  获取该学生已报的班级

    if request.method == 'POST':
        had_class = models.ClassList.objects.get(id=request.POST.get('course_grade')[0])
        where_school = request.POST.get('school', '0')
        where_school = int(where_school)

        try:
            enroll_ment = models.Enrollment.objects.get(customer=customer, course_grade=had_class, school=where_school)
            # 查看本次提交发生了改变
            # 数据库中已经存在的记录情况
            old_approved = enroll_ment.contract_approved        # False
            old_agree = enroll_ment.contract_agreed             # False
            old_memo = enroll_ment.memo                         # None
            new_approved = request.POST.get('contract_approved', False)
            if new_approved == 'on':
                new_approved = True
            new_memo = request.POST.get('memo', None)
            if old_memo != new_memo:
                enroll_ment.memo = new_memo
                enroll_ment.save()
            else:
                pass
            if new_approved:
                if not old_agree:
                    return HttpResponse(json.dumps("学员尚未完成报名"))
                if not models.PaymentRecord.objects.filter(customer=customer, classlist=had_class):
                    return HttpResponse(json.dumps("未查到学员押金交付记录"))
                else:
                    if old_approved:
                        return HttpResponse(json.dumps('该报名表已经审批通过'))
                    else:
                        # 如果未审批通过
                        if new_approved :
                            enroll_ment.contract_approved = True
                            enroll_ment.save()
                            return HttpResponse(json.dumps('审批通过'))
            else:
                return HttpResponse(json.dumps('报名报已经更新'))
        except ObjectDoesNotExist as e:
            # 此为新加报名表
            if not models.ContractTemplate.objects.filter(classlist=had_class):
                return HttpResponse(json.dumps("该课程没有对应的合同模板，请联系您的主管为该课程添加合同模板"))
            new_enrolll = models.Enrollment.objects.create(customer=customer,
                                                           course_grade=had_class,
                                                           contract_agreed=False,
                                                           contract_approved=False)
            return  HttpResponse(json.dumps("已成功添加新的报名记录"))
    else:
        enroll_ment_list = models.Enrollment.objects.filter(customer=customer, contract_approved=False)
        formes = {}
        if len(enroll_ment_list) > 0:
            for index,enroll_ment in enumerate(enroll_ment_list):
                form= forms.EnroForm(instance=enroll_ment)
                formes['form%s'% index] = form
            result = {'classes': classes, 'customer': customer, 'username': username}
            result['formes']=formes
            return render(request, 'crm/customer_enrollment.html', result)

        else:
            #print('没有报名表')
            #没有报名表，第一次进入该页面
            form = forms.EnroForm(instance=customer)
            formes['form'] =form
            result = {'classes':classes,'customer': customer,'username':username }
            result['formes']=formes
            return render(request, 'crm/customer_enrollment.html', result)


@login_required
@check_permission
def enroll_done(request, *args, **kwargs):
    customer_qq = kwargs['customer_qq']
    customer = models.Customer.objects.get(qq=customer_qq)
    all_classes = models.ClassList.objects.all()
    # 获取用户报名的所有班级，但未勾选同意的班级
    enroll_list = models.Enrollment.objects.filter(customer=customer, contract_agreed=False)
    have_class = []
    for enroll_ment in enroll_list:
        z = enroll_ment.course_grade
        have_class.append(z)

    if request.method == 'POST':
        try:
            if request.POST.get('status') == 'refuse':
                enrollments = models.Enrollment.objects.filter(
                    customer=customer,
                    contract_agreed=True,
                    contract_approved=False)
                for enrollment in enrollments:
                    enrollment.contract_agreed = False
                    enrollment.save()
                path = os.path.join(ENROLL_DATA_DIR, str(customer.id))
                shutil.rmtree(path)
                return HttpResponse(json.dumps('已经驳回该客户的报名申请'))
        except Exception as e:
            pass
        customer = models.Customer.objects.get(id=request.POST['customer'])
        new_classlist = models.ClassList.objects.get(id=request.POST.get('classlist'))
        consultant = models.UserProfile.objects.get(id=request.POST.get('consultant'))
        new_note = request.POST.get('note', None)
        new_paytype = request.POST.get('pay_type', None)
        new_paidfee = request.POST.get('paid_fee', None)
        try:
            # 以用户和所报班级 作为是否为同一张表的限制
            payment_record = models.PaymentRecord.objects.get(customer=customer, classlist=new_classlist)
            old_paytype = payment_record.pay_type
            old_paidpee = payment_record.paid_fee
            old_note = payment_record.note
            # 更新客户缴费表信息
            if old_paytype != new_paytype:
                payment_record.pay_type = new_paytype
            if old_paidpee != new_paidfee:
                payment_record.paid_fee = new_paidfee
            if old_note != new_note:
                payment_record.note = new_note
            payment_record.save()
            # 更改客户报名状态
            if new_paytype == 'deposit':
                customer.status = 'signed'
            elif new_paytype == 'tution':
                customer.status = 'paid_in_full'
            elif new_paytype == 'refund':
                customer.status = 'unregistered'
            customer.save()
            return HttpResponse(json.dumps('信息已更新'))
        except ObjectDoesNotExist as e:
            payment_records = models.PaymentRecord(
                                    customer=customer,
                                    classlist=new_classlist,
                                    pay_type=new_paytype,
                                    paid_fee=new_paidfee,
                                    note=new_note,
                                    consultant=consultant)
            # 学员新加班级,并更改客户缴费状态
            customer.class_list.add(new_classlist)
            if new_paytype == 'deposit':
                customer.status = 'signed'
            elif new_paytype == 'tution':
                customer.status = 'paid_in_full'
            elif new_paytype == 'refund':
                customer.status = 'unregistered'
            try:
                StuAccount.objects.get(stu_name=customer)
                pass
            except ObjectDoesNotExist as e:
                stu_acc_pwd = makePassword()
                stu_acc_pwd_has = hashstr(stu_acc_pwd)
                stu_acc = StuAccount.objects.create(stu_name=customer, stu_pwd=stu_acc_pwd_has)
                object = message(subject='createaccount', toaddrs=[customer.qq + '@qq.com'], )
                object.getcontent(username=customer.name, classname=payment_records.classlist,
                                  account=customer.qq, password=stu_acc_pwd)
                object.sendmessage()

            customer.save()
            payment_records.save()
            return HttpResponse(json.dumps('已创建新的报名表'))
    else:
        payment_recordss = models.PaymentRecord.objects.filter(customer=customer)
        paymentrecord_list = models.PaymentRecord.objects.filter(customer=customer)
        formes = {}
        if len(paymentrecord_list) > 0:
            for index, every_pey in enumerate(paymentrecord_list):
                form = forms.PaymentrecordForm(instance=every_pey)
                formes['form%s'% index] = form
                result = {'payment_recordss': payment_recordss, 'all_classes' :all_classes , 'have_class': have_class, 'customer': customer,}
                result['formes'] = formes
        else:
            form = forms.PaymentrecordForm(instance=customer)
            formes['form'] = form
            result = {'payment_recordss': payment_recordss, 'all_classes': all_classes, 'have_class': have_class, 'customer': customer,}
            result['formes'] = formes
        try:
            path = os.path.join(ENROLL_DATA_DIR, str(customer.id))
            files = os.listdir(path)
        except Exception:
            files = ''
        result['files'] = files
        return render(request, 'crm/customer_enroll_done.html', result)


@login_required
@check_permission
def consult_record(request, id):
    username = request.session['username']
    customer = models.Customer.objects.get(id=id)
    customer_record = models.ConsultRecord.objects.filter(customer__id=customer.id).order_by('-date')

    if request.method == 'POST':
        form = forms.AddConsultRecordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            customer.last_consult_date = datetime.datetime.now()
            customer.save()
            return HttpResponseRedirect('/crm/consult_record/%d' % customer.id)
        else:
            form = forms.AddConsultRecordForm(request.POST,instance=customer)
            return render(request, 'crm/consult_record.html', {
                'customer': customer,
                'customer_record': customer_record,
                'username': username,
                'form': form
            })
    form = forms.AddConsultRecordForm(instance=customer)
    return render(request, 'crm/consult_record.html', {
        'customer': customer,
        'customer_record': customer_record,
        'form': form,
        'username': username
    })


def login_url(request):
    next_url = request.GET.get('next')
    if next_url:
        if next_url.startswith('/crm/'):
            return my_login(request)
        if next_url.startswith('/teacher/'):
            return teacher_my_login(request)
        else:
            return my_login(request)
    else:
        return render(request, 'crm/index.html')


def my_login(request):
    curr_url = request.GET.get('next','/crm')

    error=''
    if request.method =='POST':

        result = {}
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username = cd['username'],
                password = cd['password'],
            )
            if user:
                login(request,user)
                human_username = models.UserProfile.objects.get(email=request.POST['username'])
                request.session['username']=human_username.name
                request.session['email']=request.POST['username']

                response=  HttpResponseRedirect(curr_url)
                return response
            else:
                error = '用户名或密码错误'
                form = forms.LoginForm(request.POST)

                return render(request, 'crm/login.html', {'form': form,'error':error})
        else:
            error='请输入用户名/密码'

    form = forms.LoginForm()
    return render(request,'crm/login.html',{'form':form,'error':error})


def my_logout(request):
    request.session.clear()
    return  HttpResponseRedirect(resolve_url('/crm/login'))


def error(request):
    return render(request,'crm/error.html')


@login_required
@check_permission
def customer_detail(request, id):
    username = request.session['username']
    cus = models.Customer.objects.get(id=id)
    consult_record_picture_path = CONSULT_DATA_DIR
    from_student = None
    try:
        from_student = models.Customer.objects.filter(id=cus.referral_from.id).first()
    except Exception:
        pass
    if request.method == 'POST':
        if int(request.POST.get('consultant')) == cus.consultant.id:
            form = forms.AddCustomerForm(data=request.POST, instance=cus)
            if form.is_valid():
                form.save()
                if from_student:
                    cus.referral_from = from_student
        else:
            form = forms.AddCustomerForm(data=request.POST, instance=cus)
            form.is_valid()
            form.add_error('consultant', '课程顾问选择出现错误，请刷新后重试')
    else:
        form = forms.AddCustomerForm(instance=cus)
    return render(request, 'crm/customer_detail.html', {
        'customer': cus,
        'form': form,
        'from_student': from_student,
        'picture_path': consult_record_picture_path
    })


@login_required
@check_permission
def class_list(request,*args,**kwargs):
    class_lists = models.ClassList.objects.all()
    count = models.ClassList.objects.all().count()
    return render(request,'crm/class_list.html',{'class_lists':class_lists,'count':count})


@login_required
@check_permission
def class_detail(request, *args, **kwargs):
    if request.method == 'POST':
        student_qq = request.POST.get('student_qq')
        customer=models.Customer.objects.filter(qq=student_qq).first()
        if not customer:
            return HttpResponse('客户信息有误，请刷新后重试')
        try:
            student = StuAccount.objects.get(stu_name=customer)
            stu_acc_pwd = makePassword()
            stu_acc_pwd_has = hashstr(stu_acc_pwd)
            student.stu_pwd = stu_acc_pwd_has
            student.save()


        except ObjectDoesNotExist as e:
            stu_acc_pwd = makePassword()
            stu_acc_pwd_has = hashstr(stu_acc_pwd)
            stu_acc = StuAccount.objects.create(stu_name=customer, stu_pwd=stu_acc_pwd_has)
        object = message(subject='reset_student_password', toaddrs=[customer.qq + '@qq.com'], )
        object.getcontent(username=customer.name,
                          account=customer.qq, password=stu_acc_pwd)
        object.sendmessage()
        return HttpResponse('重置密码成功')


    id = kwargs['id']
    ord=[]
    current_url = request.path
    cus_status = (('signed', '已报名'), ('paid_in_full', '学费已交齐'))  # 客户状态
    cus_status = map(lambda x: {'type': x[0], 'name': x[1]}, cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.filter(groups__name__in=consultant_list).values('email', 'name')  # 客户顾问
    staffs = map(lambda x: {'type': x['email'], 'name': x['name']}, staffs)
    staffs = list(staffs)

    res={'cus_status': cus_status, 'staffs': staffs}

    direct_org = {'class_list': id}
    page = kwargs['page']
    try:
        page = int(page)
    except:
        page = 1





    for item in kwargs.keys():
        if item !='page' and item !='id':
            if kwargs[item] != 'all':
                direct_org[item] = kwargs[item]

    for key in request.COOKIES.keys():
        if request.COOKIES[key] == 'asc' or request.COOKIES[key] == 'desc':
            if key != 'undefined':
                if request.COOKIES[key] == 'desc':
                    ord.append('-' + key)
                elif request.COOKIES[key] == 'asc':
                    ord.append(key)


    if '-date'in ord:
        ord.remove('-date')

    count = models.Customer.objects.filter(**direct_org ).count()
    pageObj = PageInfo(page, count,100)
    customers = models.Customer.objects.filter(**direct_org).order_by(*ord)[pageObj.start:pageObj.end]
    fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])

    result = {'current_url': current_url, 'customers': customers, 'count': count, 'fenye': fenye}
    result.update(res)
    return render(request, 'crm/class_detail.html', result)


@login_required
@check_permission
def Statistical(request):
    return render(request, 'crm/statistical.html')


@login_required
@check_permission
def enrollment(request, customer_id):
    customer = models.Customer.objects.filter(id=customer_id).first()

    trackers = models.UserProfile.objects.filter(consultrecord__customer__id=customer_id)
    flag = False
    if customer.consultant == request.user:
        flag = True
    for tracker in trackers:
        if tracker == request.user:
            flag = True
    if flag:
        enrollmentinformation = models.Enrollment.objects.filter(customer=customer).last()
        if enrollmentinformation:
            paymentinformation = models.PaymentRecord.objects.filter(customer=customer,
                                                                     classlist=enrollmentinformation.course_grade)
            if not paymentinformation:
                if enrollmentinformation.contract_approved == 0:
                    if enrollmentinformation.contract_agreed == 0:
                        return enrollment_agree(request, customer)
                    elif enrollmentinformation.contract_agreed == 1:
                        return enrollment_approve(request, customer)
                elif enrollmentinformation.contract_approved == 1:
                    return enrollment_payment(request, customer)
        return enrollment_add(request, customer)
    else:
        return render(request, '403_forbidden.html')


def enrollment_add(request, customer):
    status = 'add'
    customer = customer
    if request.method == 'POST':
        form = forms.EnroForm(instance=customer, data=request.POST)
        if form.is_valid():
            had_class = models.ClassList.objects.filter(id=request.POST.get('course_grade')).first()
            if not models.ContractTemplate.objects.filter(classlist=had_class):
                return HttpResponse(json.dumps("该课程没有对应的合同模板，请联系您的主管为该课程添加合同模板"))
            try:
                models.Enrollment.objects.get(customer=customer, course_grade_id=request.POST.get('course_grade'))
                return HttpResponse(json.dumps("该同学已经报名过随选的课程了，请仔细核对报名信息"))
            except Exception:
                models.Enrollment.objects.create(customer=customer, course_grade_id=request.POST.get('course_grade'),
                                                 memo=request.POST.get('memo'), school=request.POST.get('school'),
                                                 contract_agreed=0, contract_approved=0)
            return HttpResponse(json.dumps("成功添加报名表"))
        else:
            return render(request, 'crm/enrollment/enrollment_add.html', {'form': form, 'customer': customer})
    form = forms.EnroForm()
    return render(request, 'crm/enrollment/enrollment_add.html', {'form': form, 'customer': customer})


def enrollment_agree(request, customer):
    if request.method == 'POST':
        if request.POST.get('flag') == 'readd':
            enrollment_id = request.POST.get('enrollment_id')
            emrollmentinformation = models.Enrollment.objects.filter(id=enrollment_id)
            emrollmentinformation.delete()
            return HttpResponse(json.dumps('重新填写报名信息'))
    status = 'agree'
    customer = customer
    enrollment_obj = models.Enrollment.objects.filter(customer=customer, contract_agreed=0, contract_approved=0).last()
    return render(request, 'crm/enrollment/enrollment_agree.html', locals())


def enrollment_approve(request, customer):
    status = 'approve'
    file_path = ENROLL_DATA_DIR
    if request.method == 'POST':
        if request.POST.get('flag') == 'enrollment_approved':
            enrollmentinformation = models.Enrollment.objects.filter(id=request.POST.get('enrollment_id'))
            enrollmentinformation.update(contract_approved=1)
            return HttpResponse(json.dumps('该学院的审批已经通过'))
        if request.POST.get('flag') == 'enrollment_refused':
            enrollmentinformation = models.Enrollment.objects.filter(id=request.POST.get('enrollment_id'))
            enrollmentinformation.update(contract_agreed=0)
            path = os.path.join(ENROLL_DATA_DIR, str(customer.id))
            shutil.rmtree(path)
            return HttpResponse(json.dumps('已经驳回该学员的审批，请通知其重新填写'))

    customer_form = forms.CustomerForm(instance=customer)
    enrollmentinformation = models.Enrollment.objects.filter(customer=customer,
                                                             contract_agreed=1, contract_approved=0).last()
    enroll_form = forms.EnrollmentForm(instance=enrollmentinformation)
    file_path = ENROLL_DATA_DIR
    path = os.path.join(ENROLL_DATA_DIR, str(customer.id))
    files = os.listdir(path)
    return render(request, 'crm/enrollment/enrollment_approve.html', {
        'enroll_form': enroll_form,
        'customer_form': customer_form,
        'status': status,
        'files': files,
        'customer': customer,
        'enrollmentinformation': enrollmentinformation,
        'file_path': file_path,
    })


def enrollment_payment(request, customer):
    status = 'payment'
    customer = customer
    enrollmentinformation = models.Enrollment.objects.filter(customer=customer,
                                                             contract_agreed=1, contract_approved=1).last()
    if request.method == 'POST':
        form = forms.PaymentrecordForm(data=request.POST)
        if form.is_valid():
            if int(request.POST.get('paid_fee')) < 500:
                form.add_error('paid_fee', '至少需要缴费500元')
                return render(request, 'crm/enrollment/enrollment_payment.html', locals())
            else:
                customer.class_list.add(enrollmentinformation.course_grade)
                customer.status = 'signed'
                customer.save()
                payment_obj = models.PaymentRecord.objects.create(customer=customer, consultant=request.user,
                                                                  classlist_id=request.POST.get('classlist'),
                                                                  pay_type=request.POST.get('pay_type'),
                                                                  paid_fee=request.POST.get('paid_fee'),
                                                                  note=request.POST.get('note'),)
                try:
                    StuAccount.objects.get(stu_name=customer)
                except ObjectDoesNotExist as e:
                    stu_acc_pwd = makePassword()
                    stu_acc_pwd_has = hashstr(stu_acc_pwd)
                    stu_acc = StuAccount.objects.create(stu_name=customer, stu_pwd=stu_acc_pwd_has)
                    object = message(subject='createaccount', toaddrs=[customer.qq + '@qq.com'], )
                    object.getcontent(username=customer.name, classname=payment_obj.classlist,
                                      account=customer.qq, password=stu_acc_pwd)
                    object.sendmessage()
                if not customer.consultant == request.user:
                    models.ConsultRecord.objects.create(customer=customer, note='因报名而更换课程顾问，原课程顾问为{},更换为{}'.format(customer.consultant, request.user), status=7, consultant=request.user)
                    customer.consultant = request.user
                    customer.save()
                if enrollmentinformation.course_grade.class_type == 'pick_up_study':
                    courserecord = models.CourseRecord.objects.filter(course=enrollmentinformation.course_grade, day_num=1).first()
                    models.OnlineStuAssignment.objects.get_or_create(enrollment=enrollmentinformation, schedule=courserecord)
                return redirect(reverse('signed', args=('all', 'all', 'all', 'all', 'all', 'all', 1)))
        else:
            return render(request, 'crm/enrollment/enrollment_payment.html', locals())

    form = forms.PaymentrecordForm()
    return render(request, 'crm/enrollment/enrollment_payment.html', locals())

@login_required
@check_permission
def payment(request, payment_id):
    payment_id = payment_id
    paymentinformation = models.PaymentRecord.objects.filter(id=payment_id).first()
    customer = paymentinformation.customer
    if request.method == 'POST':
        form = forms.PaymentrecordForm(instance=paymentinformation, data=request.POST)
        if form.is_valid():
            if int(request.POST.get('paid_fee')) < 500:
                form.add_error('paid_fee', '至少需要缴费500元')
                return render(request, 'crm/payment.html', {
                    'paymentinformation': paymentinformation,
                    'form': form,
                    'customer': customer
                })
            else:
                if request.POST.get('pay_type') == 'tution':
                    try:
                        models.PaymentRecord.objects.get(customer=customer, pay_type='deposit')
                        customer.status = 'signed'
                    except Exception:
                        customer.status = 'paid_in_full'
                elif request.POST.get('pay_type') == 'deposit':
                    customer.status = 'signed'
                elif request.POST.get('pay_type') == 'refund':
                    customer.status = 'unregistered'
                    try:
                        models.PaymentRecord.objects.get(customer=customer, pay_type='tution')
                        customer.status = 'paid_in_full'
                    except Exception:
                        try:
                            models.PaymentRecord.objects.get(customer=customer, pay_type='deposit')
                            customer.status = 'signed'
                        except Exception:
                            pass
                customer.save()
                form.save()
        else:
            return render(request, 'crm/payment.html', {
                'paymentinformation': paymentinformation,
                'form': form,
                'customer': customer
            })
    form = forms.PaymentrecordForm(instance=paymentinformation)
    return render(request, 'crm/payment.html', {
        'paymentinformation': paymentinformation,
        'form': form,
        'customer': customer
    })


@login_required
@check_permission
def punishment(request):
    rules = models.Rules.objects.all()
    student_qq = request.GET.get('student_qq')
    if not student_qq:
        enrollments = None
    else:
        enrollments = models.Enrollment.objects.filter(customer__qq=student_qq)
        if not enrollments:
            error_message_qq = '未查询到该QQ号的学生资料'
        else:
            punishments= models.StuPunishmentRecord.objects.filter(enrollment__customer__qq=student_qq)
    if request.method == 'POST':
        create_dict = {}
        enrollment_id = request.POST.get('enrollment',None)
        if enrollment_id:
            enrollment_id = int(enrollment_id)
        rule_id = request.POST.get('rule', None)
        if rule_id:
            rule_id = int(rule_id)
        note = request.POST.get('note')
        if enrollment_id:
            create_dict['enrollment_id'] = enrollment_id
            if rule_id:
                create_dict['rule_id'] = rule_id
                if note:
                    create_dict['note'] = note
                date = request.POST.get('date')
                if date:
                    create_dict['date'] = date.replace('年', '-').replace('月', '-').replace('日', '')
                create_dict['performer'] = request.user
                models.StuPunishmentRecord.objects.create(**create_dict)
                return HttpResponse('已经添加了该学员的违规记录')
            else:
                error_message_rule = '请选择该学员违反的规则'
        else:
            error_message_enrollment = '请先选择违纪的学生信息'
    return render(request, 'crm/punishment.html', locals())