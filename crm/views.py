#_*_coding:utf-8_*_
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect,resolve_url
from django.core.urlresolvers import resolve
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from crm import models
import json,os,random,zipfile,datetime
from crm import survery_handle
from crm import class_grade
from crm import forms
from django.db.models import Sum,Count
from OldboyCRM import settings
from django.http import FileResponse
from django.utils.encoding import smart_str
from django.contrib.auth import login,logout,authenticate
from crm.html_helper import PageInfo,Page
from crm.myauth import UserProfile  


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
        #print(dir(request))
        client_id =  request.COOKIES.get("csrftoken")
        #print request.environ 8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM
        #print request.environ 8Jilt6JfSO0XCVe2oMViKbbV1faEI2KM

        form_data = json.loads(request.POST.get("data"))
        survery_handler = survery_handle.Survery(client_id,survery_id,form_data)
        if survery_handler.is_valid():
            survery_handler.save()

        else:
            pass
            #print(survery_handler.errors)
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
        #print("---qualify benchmark ", qualifiy_benchmark)

        #加上排名
        class_grade_dic[class_obj.id]['record_count'] = sorted(class_grade_dic[class_obj.id]['record_count'],key=lambda x:x[2])
    #print(class_grade_dic)
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
        #print('filelist',file_list)
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

        
        
@login_required
def dashboard(request):
    email = request.session['email']
    dict_org={'consultant__email':email,'status':'unregistered'}
    cus=models.Customer.objects.filter(**dict_org)
    today= datetime.date.today()
    customers=[]
    result = {}
    for customer in cus:

        last_consult=customer.consultrecord_set.last()  #最后跟进记录

        if last_consult == None: #无跟进记录，以录入日期为准
            consultant_date = customer.date  #  录入日期
            midd_date = today - consultant_date  # 录入日期距 今天多久
            max_day = datetime.timedelta(days=15)  # 预期最大间隔时间
            if midd_date <= max_day:  # 距今间隔 < 预期间隔
                customers.append(customer)   # 只截取最近15天内的跟进客户

        else:  #有跟进记录,以最后跟进记录日期为准
            last_date = customer.consultrecord_set.last().date  # 最后跟进日期
            midd_date = today - last_date  # 最后跟进日期距 今天多久
            max_day = datetime.timedelta(days=15)  # 预期最大间隔时间，
            if midd_date <= max_day:   #距今间隔 < 预期间隔
                customers.append(customer)  #只截取最近15天内的跟进客户

    random.shuffle(customers) # 打乱客户随机顺序
    customers=customers[0:5]   # 只截取需跟进库的前5名
    count = len(customers)
    succe_track = {'customers':customers,'count':count}
    result.update(succe_track)

    # 以下为 销量排名图表 所需数据
    sales=[(i.email,i.name) for i in models.UserProfile.objects.all() if not i.is_staff]
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
        b =count_all(sale_track,sale_signed)
        a = [sale_track,sale_signed]
        a.extend(b)
        sale_num[sale[1]] =a
    print('sale_num-->> ',sale_num)

    b = True
    curr_url = request.path
    z = int(request.GET.get('o',1))


    sale_list = sorted(sale_num.items(),key=lambda x:x[1][z],reverse=b)[0:5]   # 筛选 签约客户量 前 N 名

    result['sale_list']=sale_list
    result['curr_url']=curr_url
    return render(request,'crm/dashboard.html',result)


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
            sale_track = models.Customer.objects.filter(status='unregistered', consultant__email=sale.email,
                                                        date__gt=month_before, date__lt=today).count()  # 本月至今 正跟进客户数
            sale_signed = models.Customer.objects.exclude(status='unregistered').filter(consultant__email=sale.email,
                                                                                        date__gt=month_before,
                                                                                        date__lt=today).count()  # 本月至今 已签约客户数
            sale_num[sale.name] = [sale_track, sale_signed,sale_track+sale_signed]

        sale_dict=json.dumps(sale_num)
        return HttpResponse(sale_dict)






@login_required
def tracking(request,page,*args,**kwargs):
    ord = []
    username = request.session['username']
    user = request.user

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
    print('cus_status ',cus_status)
    cus_status = map(lambda x: {'type': x[0], 'name': x[1]}, cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.filter(email=user).values('email', 'name')  # 客户顾问
    staffs = map(lambda x: {'type': x['email'], 'name': x['name']}, staffs)
    staffs = list(staffs)

    filter_date = [{'type': 'today', 'name': '今天'}, {'type': 'sevendays', 'name': '七天以内'},
                   {'type': 'month', 'name': '本月'}, {'type': 'year', 'name': '今年'}]

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

    direct_org = {'consultant__email': user,'status': 'unregistered'}

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
            else:
                direct_org['date__gte'] = ayearbef
                direct_org['date__lt'] = today

        else:
            if kwargs[item] != 'all':
                direct_org[item] = kwargs[item]



    if GET.get('qq'):
        qq_num_err={}
        qq = GET['qq']
        try:
            qq = int(qq)
        except ValueError as e:
            qq_num_err={'qq_num_error':'只能输入QQ号'}


        direct_org.update({'qq':qq})

        customers = models.Customer.objects.filter(**direct_org)
        count = models.Customer.objects.filter(**direct_org).count()
        fil = {'customers': customers, 'count': count,}
        fil.update(qq_num_err)
        result.update(fil)

    else:

        try:
            page = int(page)
        except:
            page = 1

        print('cookie-->> ', request.COOKIES)

        for key in request.COOKIES.keys():
            # print('val-- ',val)
            if request.COOKIES[key] == 'asc' or request.COOKIES[key] == 'desc':
                if key != 'undefined':
                    if request.COOKIES[key] == 'desc':
                        ord.append('-' + key)
                    elif request.COOKIES[key] == 'asc':
                        ord.append(key)

        count = models.Customer.objects.filter(**direct_org).count()
        pageObj = PageInfo(page, count, 3)
        customers = models.Customer.objects.filter(**direct_org).select_related().order_by(*ord)[pageObj.start:pageObj.end]
        fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])

        fil = {'customers': customers, 'count': count, 'fenye': fenye}

        result.update(fil)
    return render(request, 'crm/tracking.html', result)


@login_required
def signed(request,page,*args,**kwargs):
    ord = []
    if request.method == 'POST':
        id=request.POST['id']
        cur_customer = models.Customer.objects.get(id=id)

        if request.POST['cus_sta']=='paid_in_full':
            cur_customer.status='paid_in_full'
            cur_customer.save()


    username = request.session['username']
    user = request.user
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

    cus_status = (('signed', '已报名'),('paid_in_full', '学费已交齐'))  # 客户状态
    cus_status = map(lambda x: {'type': x[0], 'name': x[1]}, cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.filter(email=user).values('email', 'name')  # 客户顾问
    staffs = map(lambda x: {'type': x['email'], 'name': x['name']}, staffs)
    staffs = list(staffs)

    filter_date = [{'type': 'today', 'name': '今天'}, {'type': 'sevendays', 'name': '七天以内'},
                   {'type': 'month', 'name': '本月'}, {'type': 'year', 'name': '今年'}]

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
    exc = {'status':'unregistered'}
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
            else:
                direct_org['date__gte'] = ayearbef
                direct_org['date__lt'] = today

        else:
            if kwargs[item] != 'all':
                direct_org[item] = kwargs[item]


    if GET.get('qq'):
        qq_num_err={}
        qq = GET['qq']
        try:
            qq = int(qq)
        except ValueError as e:
            qq_num_err = {'qq_num_error': '只能输入QQ号'}

        direct_org.update({'qq': qq})
        print('dire__',direct_org)
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


        for key in request.COOKIES.keys():

            if request.COOKIES[key] == 'asc' or request.COOKIES[key] == 'desc':
                if key != 'undefined':
                    if request.COOKIES[key] == 'asc':
                        ord.append(key)
                    elif request.COOKIES[key] == 'desc':
                        ord.append('-' + key)

        count = models.Customer.objects.filter(**direct_org).exclude(**exc).count()
        pageObj = PageInfo(page, count, 3)


        customers = models.Customer.objects.filter(**direct_org).exclude(**exc).select_related().order_by(*ord)[pageObj.start:pageObj.end]
        fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])

        fil = {'customers': customers, 'count': count, 'fenye': fenye}

        result.update(fil)
    return render(request, 'crm/signed.html', result)




@login_required
def customers_library(request,page,*args,**kwargs):
    ord = []
    print(page, args,kwargs)
    username = request.session['username']
    current_url = request.path
    GET = request.GET


    cus_sources = models.Customer.source_type  # 以客户来源
    cus_sources =map(lambda x:{'type':x[0],'name':x[1]},cus_sources)
    cus_sources = list(cus_sources)

    course = models.course_choices  # 以咨询课程
    course =map(lambda x:{'type':x[0],'name':x[1]},course)
    course = list(course)

    classes = models.class_type_choices  # 以班级类型
    classes =map(lambda x:{'type':x[0],'name':x[1]},classes)
    classes = list(classes)

    cus_status = models.Customer.status_choices  # 客户状态
    cus_status =map(lambda x:{'type':x[0],'name':x[1]},cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.all().values('email','name')  #客户顾问
    staffs = map(lambda x:{'type':x['email'],'name':x['name']},staffs )
    staffs = list(staffs)

    filter_date = [{'type':'today','name':'今天'},{'type':'sevendays','name':'七天以内'},{'type':'month','name':'本月'},{'type':'year','name':'今年'}]

    result ={
        'cus_sources':cus_sources,
        'course':course,
        'classes':classes,
        'cus_status':cus_status,
        'staffs':staffs,
        'current_url':current_url,
        'filter_date':filter_date,
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

        if item == 'filter_date':  #单独对日期进行处理
            if kwargs[item] =='all':
                pass
            elif kwargs[item] == 'today':
                direct_org['date'] = today
            elif kwargs[item] == 'sevendays':
                direct_org['date__gte'] = sevendaybef
                direct_org['date__lt'] = today
            elif kwargs[item] =='month':
                direct_org['date__gte'] = amouthbef
                direct_org['date__lt'] = today
            else:
                direct_org['date__gte'] = ayearbef
                direct_org['date__lt'] = today

        else:
            if kwargs[item] != 'all':
                direct_org[item] = kwargs[item]

    if GET.get('qq'):
        qq_num_err={}
        qq = GET['qq']
        try:
            qq = int(qq)
        except ValueError as e:
            qq_num_err = {'qq_num_error': '只能输入QQ号'}
        print('qq-- ',qq,type(qq))
        customers = models.Customer.objects.filter(qq=qq)
        count = models.Customer.objects.filter(qq=qq).count()
        fil = {'customers': customers, 'count': count,}
        fil.update(qq_num_err)

    else:
        try:
            page = int(page)
        except:
            page = 1


        count = models.Customer.objects.filter(**direct_org).count()
        print(page,type(page),count)


        try:
            page = int(page)
        except:
            page = 1
        pageObj = PageInfo(page, count, 50)

        print('cookie-->> ',request.COOKIES)
        for key in request.COOKIES.keys():

            if request.COOKIES[key]=='asc' or request.COOKIES[key] =='desc':
                if key !='undefined':
                    if request.COOKIES[key] == 'asc':

                        ord.append(key)
                    elif request.COOKIES[key]=='desc':

                        ord.append('-'+key)

        print('ord===>> ',ord)
        customers = models.Customer.objects.filter(**direct_org).select_related().order_by(*ord)[pageObj.start:pageObj.end]
        fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])
        # print('path -->> ',current_url)


        fil = {'customers':customers,'count':count,'fenye':fenye}

    result.update(fil)
    return render(request, 'crm/customers_library.html', result)

@login_required
def addcustomer(request):
    username = request.session['username']
    curr_user = models.UserProfile.objects.get(name=username)
    if request.method == 'POST':
        form = forms.AddCustomerForm(request.POST)
        print('form-->> ',form)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect(resolve_url('tracking','all', 'all', 'all', 'all', 'all','all','1'))
        else:
            form = forms.AddCustomerForm(data=request.POST)
            return render(request, 'crm/addcustomer.html', {'form': form, 'username': username,'curr_user':curr_user})
    form = forms.AddCustomerForm()
    return render(request,'crm/addcustomer.html',{'form':form,'username':username,'curr_user':curr_user})

@login_required
def cus_enroll(request,id):
    username = request.session['username']
    customer = models.Customer.objects.get(id=id)
    classes = models.ClassList.objects.all()


    try:
        customer.enrollment_set.select_related()
        enroll_ment = models.Enrollment.objects.get(customer=customer)
    except Exception as e:
        enroll_ment = None
    if request.method == 'POST':
        print('post  ',request.POST)
        if enroll_ment:
            try:
                customer.status=request.POST['status']
                customer.save()
                post = request.POST.copy()
                customer.class_list=request.POST['course_grade']
                customer.save()
                post['contract_agreed']=True
                form = forms.EnroForm(data=post,instance=enroll_ment)
                print('from-->> ',form)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(resolve_url('enroll_done',customer.qq))
            except Exception as e:
                return HttpResponseRedirect(resolve_url('error'),{'error':'error'})

        else:
            #销售第一次登记学员报名信息，等待学员同意
            post = request.POST.copy()
            post['status']='unregistered'
            print('post--',post)
            form = forms.EnroForm(data=post)
            print('form---   ',form)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/crm/enroll_done/%s/'% customer.qq)

    else:

        if enroll_ment is None:

            # 如果没有报名表
            form = forms.EnroForm(instance=customer)

            result = {'classes':classes,'form': form, 'customer': customer,'username':username }
            return render(request, 'crm/customer_enrollment.html', result)

        else:

            # 如果已有报名表，等待审核
            form = forms.EnroForm(instance=enroll_ment)
            print('form-->> ',form)
            result = {'form': form, 'customer': customer, 'enroll_ment': enroll_ment, 'username': username,'classes':classes}
            return render(request, 'crm/customer_enrollment.html', result)




@login_required
def enroll_done(request,qq):
    username = request.session['username']
    customer = models.Customer.objects.get(qq=qq)
    payment_records = models.PaymentRecord.objects.select_related().filter(customer__qq=customer.qq)


    if request.method == 'POST':
        print('POST---',request.POST)
        form = forms.PaymentrecordForm(request.POST)
        if form.is_valid():

            customer.course = request.POST['course']
            customer.class_type = request.POST['class_type']
            if request.POST['pay_type'] =='tution':
                customer.status='paid_in_full'
                customer.save()
            elif request.POST['pay_type'] == 'deposit':
                customer.status = 'signed'
                customer.save()
            elif request.POST['pay_type'] == 'refund':
                customer.status = 'unregistered'
                customer.save()
            form.save()
            return HttpResponseRedirect(resolve_url('enroll_done',customer.qq))

    form = forms.PaymentrecordForm(instance=customer)
    return render(request,'crm/customer_enroll_done.html',{'username':username,'form':form,'payment_records':payment_records,'customer':customer})

@login_required
def consult_record(request,id):
    username = request.session['username']
    customer = models.Customer.objects.get(id=id)
    customer_record = models.ConsultRecord.objects.filter(customer__id=customer.id).order_by('-date')


    if request.method == 'POST':
        form = forms.AddConsultRecordForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # if cd['consultant'].email == request.session['email']:
            form.save()
            return HttpResponseRedirect('/crm/consult_record/%d' % (customer.id))
            # else:
            #     return render(request,'crm/error.html',{'error':"只能修改自己的客户！"})
        else:

            form = forms.AddConsultRecordForm(request.POST,instance=customer)
            return render(request,'crm/consult_record.html',{'customer':customer,'customer_record':customer_record,'username':username,'form':form})
    form = forms.AddConsultRecordForm(instance=customer)

    return render(request,'crm/consult_record.html',{'customer':customer,'customer_record':customer_record,'form':form,'username':username})



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
def customer_detail(request,id):
    username = request.session['username']
    cus =models.Customer.objects.get(id=id)
    curr_user = models.UserProfile.objects.get(name=username)
    if request.method == 'POST':
        form= forms.AddCustomerForm(data=request.POST,instance=cus)
        if form.is_valid():
            form.save()

    else:

        form = forms.AddCustomerForm(instance=cus)
    return render(request,'crm/customer_detail.html',{'customer':cus,'form':form,'curr_user':curr_user})

@login_required
def class_list(request,*args,**kwargs):
    class_lists = models.ClassList.objects.all()
    count = models.ClassList.objects.all().count()
    # students = models.Customer.objects.filter(class_list=).count()
    return render(request,'crm/class_list.html',{'class_lists':class_lists,'count':count})

@login_required
def class_detail(request,*args,**kwargs):
    id = kwargs['id']
    ord=[]
    current_url = request.path
    print('kwargs',kwargs)
    cus_status = (('signed', '已报名'), ('paid_in_full', '学费已交齐'))  # 客户状态
    cus_status = map(lambda x: {'type': x[0], 'name': x[1]}, cus_status)
    cus_status = list(cus_status)

    staffs = models.UserProfile.objects.all().values('email', 'name')  # 客户顾问
    staffs = map(lambda x: {'type': x['email'], 'name': x['name']}, staffs)
    staffs = list(staffs)

    res={'cus_status':cus_status,'staffs':staffs}

    direct_org={'class_list':id}
    page= kwargs['page']
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
    print('dict', ord)

    count = models.Customer.objects.filter(**direct_org ).count()
    pageObj = PageInfo(page, count,50)
    customers = models.Customer.objects.filter(**direct_org).order_by(*ord)[pageObj.start:pageObj.end]
    fenye = Page(page, pageObj.all_page_count, url_path=current_url[0:-2])

    result={'current_url':current_url,'customers':customers,'count':count,'fenye':fenye}
    result.update(res)
    return render(request,'crm/class_detail.html',result)


def Statistical(request):
    return render(request,'crm/statistical.html')

