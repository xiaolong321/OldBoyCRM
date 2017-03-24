from django.shortcuts import render, HttpResponse, HttpResponseRedirect, resolve_url
from django.contrib.auth.decorators import login_required
from teacher import models
from crm.permissions import check_permission
from OldboyCRM.settings import HOMEWORK_DATA_DIR, ATTENDANCE_DATA_DIR
from teacher import forms
from crm import forms as crm_forms
from django.contrib.auth import login, logout, authenticate
import os
from crm import views as crm_views
import zipfile
from OldboyCRM import settings
import xlwt


# Create your views here.

def changenumtochar(num):           # 将数字转换为以A-Z表示的26进制的字母表现形式，以供写Excel的公式时的定位使用
    quotient, remainder = divmod(num-1, 26)
    if quotient > 26:
        a = changenumtochar(quotient)
    elif quotient == 0:
        a = ''
    else:
        a = chr(quotient + ord('A')-1)
    b = chr(remainder + ord('A'))
    return (a+b)


def my_login(request):
    curr_url = request.GET.get('next','/teacher')
    error=''
    if request.method =='POST':
        result = {}
        form = crm_forms.LoginForm(request.POST)
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

                response = HttpResponseRedirect(curr_url)
                return response
            else:
                error = '用户名或密码错误'
                form = crm_forms.LoginForm(request.POST)

                return render(request, 'teacher/login.html', {'form': form,'error':error})
        else:
            error='请输入用户名/密码'
    form = crm_forms.LoginForm()
    return render(request,'teacher/login.html',{'form':form,'error':error})


def my_logout(request):
    request.session.clear()
    return  HttpResponseRedirect(resolve_url('/teacher/login'))


@login_required
@check_permission
def dashboard(request):
    return render(request, 'teacher/dashboard.html')


@login_required
@check_permission
def classlist(request):
    if request.method == 'GET':
        classlists = models.ClassList.objects.filter(teachers=request.user)
        return render(request, 'teacher/classlist.html', locals())


@login_required
@check_permission
def courselist(request, class_id):
    class_obj = models.ClassList.objects.filter(id=class_id).first()
    if request.method == 'POST':
        # 设置文件导出位置及文件名
        # savefile = ('D:\linux_s31_kaoqin.xls')
        savefile = ('{}/{}/{}{}.xls'.format(ATTENDANCE_DATA_DIR, class_id, class_obj.course, class_obj.semester))
        # if os.path.exists(savefile):
        #     os.remove(savefile)
        if not os.path.exists(os.path.dirname(savefile)):
            os.makedirs(os.path.dirname(savefile))

        # 设置要查询的表，其中要显示的列请勿动。
        # 得到数据样式   （签到情况，学员姓名，第几天课程）
        data = models.StudyRecord.objects.filter(course_record__course_id=class_id).values('course_record__date',
                                                                                           'course_record__day_num',
                                                                                           'student__name',
                                                                                           'record',
                                                                                           'score',
                                                                                           'homework_note',)

        xls = xlwt.Workbook(encoding="utf-8")  # 创建一个xls对象
        sheet1 = xls.add_sheet('考勤表', cell_overwrite_ok=True)  # 给 xls 添加一张‘考勤表’的表格
        sheet2 = xls.add_sheet('成绩表', cell_overwrite_ok=True)  # 给 xls 添加一张‘成绩表’的表格
        # sheet.write(行，列，'内容') !!!行、列均是从 0 0 开始计数
        x = 0  # 初始化表格的行
        y = 0  # 初始化表格的列
        students = {}  # 内含所有学员名 {姓名：第几天,}     {'李四': 3, }
        courseday = []  # 内含所有课程天数
        status1 = {'checked': '已签到', 'late': '迟到', 'noshow': '缺勤', 'leave_early': '早退'}
        status2 = {100: 'A+', 90: 'A', 85: 'B+', 80: 'B', 70: 'B-', 60: 'C+', 50: 'C', 40: 'C-', 0: 'D', -1: 'N/A', -100: 'COPY', -1000: 'FAIL'}
        print(data)
        for one in data:
            print(one)
            if one['course_record__day_num'] not in courseday:
                y = one['course_record__day_num']
                courseday.append(y)
                sheet1.write(0, y, '{}第{}天签到情况'.format(one['course_record__date'], y))
                sheet2.write(0, 2*y-1, '{}第{}天作业成绩'.format(one['course_record__date'], y))
                sheet2.write(0, 2*y, '{}第{}天作业批注'.format(one['course_record__date'], y))

            if one['student__name'] not in students:
                # 学员不在students列表内\
                x += 1
                students.setdefault(one['student__name'], x)
                sheet1.write(x, 0, one['student__name'])
                sheet2.write(x, 0, one['student__name'])
        for one in data:
            if not one['student__name'] not in students:
                for i in courseday:
                    if i == one['course_record__day_num']:
                        for sta1 in status1:  # 改英文为中文，显示学员签到情况
                            if sta1 == one['record']:
                                sheet1.write((students[one['student__name']]), (i), status1[sta1])
                        for sta2 in status2:
                            if sta2 == one['score']:
                                sheet2.write((students[one['student__name']]), (2*i-1), status2[sta2])
                                sheet2.write((students[one['student__name']]), (2*i), one['homework_note'])
        sheet1.write(0, y+1, '迟到次数')
        sheet1.write(0, y+2, '早退次数')
        sheet1.write(0, y+3, '缺勤次数')
        sheet1.write(0, y+4, '正常签到次数')
        sheet2.write(0, 2*y+1, '获得A+次数')
        sheet2.write(0, 2*y+2, '获得A次数')
        sheet2.write(0, 2*y+3, '获得B+次数')
        sheet2.write(0, 2*y+4, '获得B次数')
        sheet2.write(0, 2*y+5, '获得B-次数')
        sheet2.write(0, 2*y+6, '获得C+次数')
        sheet2.write(0, 2*y+7, '获得C次数')
        sheet2.write(0, 2*y+8, '获得C-次数')
        sheet2.write(0, 2*y+9, '获得D次数')
        sheet2.write(0, 2*y+10, '获得COPY次数')
        sheet2.write(0, 2*y+11, '获得FAIL次数')
        for i in range(0,x):
            sheet1.write(i+1, y+1, xlwt.Formula('COUNTIF({}{}:{}{},"迟到")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet1.write(i+1, y+2, xlwt.Formula('COUNTIF({}{}:{}{},"早退")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet1.write(i+1, y+3, xlwt.Formula('COUNTIF({}{}:{}{},"缺勤")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet1.write(i+1, y+4, xlwt.Formula('COUNTIF({}{}:{}{},"已签到")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+1, xlwt.Formula('COUNTIF({}{}:{}{},"A+")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+2, xlwt.Formula('COUNTIF({}{}:{}{},"A")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+3, xlwt.Formula('COUNTIF({}{}:{}{},"B+")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+4, xlwt.Formula('COUNTIF({}{}:{}{},"B")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+5, xlwt.Formula('COUNTIF({}{}:{}{},"B-")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+6, xlwt.Formula('COUNTIF({}{}:{}{},"C+")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+7, xlwt.Formula('COUNTIF({}{}:{}{},"C")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+8, xlwt.Formula('COUNTIF({}{}:{}{},"C-")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+9, xlwt.Formula('COUNTIF({}{}:{}{},"D")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+10, xlwt.Formula('COUNTIF({}{}:{}{},"COPY")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
            sheet2.write(i+1, 2*y+11, xlwt.Formula('COUNTIF({}{}:{}{},"FAIL")'.format(changenumtochar(2), i+2, changenumtochar(y+1), i+2)))
        xls.save(savefile)
        return HttpResponse('下载文件准备就绪')

    else:
        if class_obj.class_type == 'pick_up_study':
            student_list = models.OnlineStuAssignment.objects.filter(enrollment__course_grade=class_obj,
                                                            assistant__name__email=request.user.email)
            return render(request, 'teacher/online_student_list.html', locals())
        else:
            attendance_path = ATTENDANCE_DATA_DIR
            courselist = models.CourseRecord.objects.filter(course_id=class_id, course__teachers=request.user)
            return render(request, 'teacher/courselist.html', locals())


@login_required
@check_permission
def coursedetail(request, class_id):
    courserecords = models.CourseRecord.objects.filter(course_id=class_id)
    return render(request, 'teacher/coursedetail.html', locals())


@login_required
@check_permission
def courserecord(request, course_id, student_id=None):
    if request.method == 'GET':

        homework_path = HOMEWORK_DATA_DIR
        if not student_id == '0':
            OnlineStuAssignment = models.OnlineStuAssignment.objects.filter(
                enrollment__customer_id=student_id, enrollment__course_grade_id=course_id).first()
            day_num = OnlineStuAssignment.schedule.day_num
            class_obj = models.ClassList.objects.filter(id=course_id).first()
            studyrecords = models.StudyRecord.objects.filter(course_record__course=class_obj, student_id=student_id)
            if len(studyrecords) == 0:
                courserecord = models.CourseRecord.objects.filter(course=class_obj, day_num=1).first()
                studyrecords = [models.StudyRecord.objects.create(course_record=courserecord, student_id=student_id,)]
            return render(request, 'teacher/online_course_record.html', locals())
        else:
            class_id = course_id
            courserecord = models.CourseRecord.objects.filter(id=class_id).first()
            status = request.GET.get('status')
            filter_dic = {}
            filter_dic['course_record_id'] = class_id
            filter_dic['course_record__course__teachers'] = request.user
            if status == 'sieve':
                record_sieve = request.GET.get('record_sieve')
                score_sieve = request.GET.get('score_sieve')
                if not record_sieve == 'all':
                    filter_dic['record'] = record_sieve
                if not score_sieve == 'all':
                    filter_dic['score'] = score_sieve
                studyrecords = models.StudyRecord.objects.filter(**filter_dic)
                return render(request, 'teacher/courserecord.html', locals())
            else:
                record_sieve = 'all'
                score_sieve = 'all'
                studyrecords = models.StudyRecord.objects.filter(**filter_dic)
                return render(request, 'teacher/courserecord.html', locals())

    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'homework_download':
            customer_file_path = request.POST.get('file_path')
            filename = '%s.zip' % customer_file_path.split('/')[-1]
            zipfile_path = "%s/%s" % (settings.HOMEWORK_DATA_DIR, customer_file_path.split('/')[-2])
            zipfile_obj = zipfile.ZipFile("%s/%s" % (zipfile_path, filename), 'w', zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk(os.path.join(customer_file_path, 'all')):
                for file in filenames:
                    zipfile_obj.write(os.path.join(dirpath, file),
                                      os.path.join(dirpath.split(os.path.join(customer_file_path, 'all'))[-1], file))
            zipfile_obj.close()
            return HttpResponse('下载文件准备就绪')
        if status == 'test_pass':
            OnlineStuAssignment = models.OnlineStuAssignment.objects.filter(enrollment__customer_id=student_id,
                                                          enrollment__course_grade_id=course_id).first()
            day_num = OnlineStuAssignment.schedule.day_num + 1
            try:
                courserecord = models.CourseRecord.objects.get(course_id=course_id, day_num=day_num)
            except Exception:
                OnlineStuAssignment.status = 'graduate'
                OnlineStuAssignment.save()
                return HttpResponse('该学生已经学完了全部的内容')
            OnlineStuAssignment.schedule = courserecord
            OnlineStuAssignment.save()
            models.StudyRecord.objects.get_or_create(course_record=courserecord, student_id=student_id)
            return HttpResponse('该学生完成了当前部分内容的学习')
        else:
            student_id = request.POST.get('student_id',)
            course_id = request.POST.get('course_id', )
            information = request.POST.get('information')
            studyrecord = models.StudyRecord.objects.filter(course_record_id=course_id, student_id=student_id,)

            if studyrecord:
                up_dict = {status:information}
                studyrecord.update(**up_dict)
                studyrecord = studyrecord.first()
            else:
                create_dict ={
                    'course_record_id':course_id,
                    'student_id':student_id,
                    status:information,
                }
                studyrecord = models.StudyRecord.objects.create(**create_dict)
            if status == 'record':
                if information == 'checked':
                    try:
                        stupunishmentrecord = models.StuPunishmentRecord.objects.get(studyrecord=studyrecord,
                                                                                     note='根据学生出席情况自动创建')
                        stupunishmentrecord.delete()
                    except Exception:
                        pass
                else:
                    if information == 'vacate':
                        rule = models.Rules.objects.get(name='请假')
                    if information == 'late':
                        rule = models.Rules.objects.get(name='迟到')
                    if information == 'noshow':
                        rule = models.Rules.objects.get(name='缺勤')
                    if information == 'leave_early':
                        rule = models.Rules.objects.get(name='早退')
                    try:
                        stupunishmentrecord = models.StuPunishmentRecord.objects.get(studyrecord=studyrecord,
                                                                                     note='根据学生出席情况自动创建')
                        stupunishmentrecord.rule = rule
                        stupunishmentrecord.save()
                    except Exception:
                        enrollment = models.Enrollment.objects.get(course_grade=studyrecord.course_record.course,
                                                                      customer=studyrecord.student)
                        stupunishmentrecord = models.StuPunishmentRecord.objects.create(
                            enrollment=enrollment, rule=rule, performer=request.user,
                            note='根据学生出席情况自动创建', studyrecord=studyrecord)

            if status == 'score':
                information = int(information)
                if information >= 60:
                    try:
                        stupunishmentrecord = models.StuPunishmentRecord.objects.get(studyrecord=studyrecord,
                                                                                     note='根据学生成绩情况自动创建')
                        stupunishmentrecord.delete()
                    except Exception:
                        pass
                else:
                    if information < 60:
                        rule = models.Rules.objects.get(name='作业不及格')
                    if information <= 0:
                        rule = models.Rules.objects.get(name='不交作业')
                    if studyrecord.course_record.has_homework:
                        try:
                            stupunishmentrecord = models.StuPunishmentRecord.objects.get(studyrecord=studyrecord,
                                                                                         note='根据学生成绩情况自动创建')
                            stupunishmentrecord.rule = rule
                            stupunishmentrecord.save()
                        except Exception as e:
                            print(e)
                            enrollment = models.Enrollment.objects.get(course_grade=studyrecord.course_record.course,
                                                                       customer=studyrecord.student)
                            stupunishmentrecord = models.StuPunishmentRecord.objects.create(
                                enrollment=enrollment,rule=rule, performer=request.user,
                                note='根据学生成绩情况自动创建', studyrecord=studyrecord)
            return HttpResponse('OK')


@login_required
@check_permission
def createcourse(request, class_id, courserecord_id=None):
    if request.method == 'GET':
        if courserecord_id:
            courserecord = models.CourseRecord.objects.get(course_id=class_id, id=courserecord_id)
            form = forms.CourserecordForm(instance=courserecord)
            return render(request, 'teacher/editcourse.html', locals())
        else:
            flag = models.CourseRecord.objects.filter(course_id=class_id, course__teachers=request.user).order_by('day_num').last()
            if flag:
                day_num = flag.day_num + 1
            else:
                day_num = 1
            form = forms.CourserecordForm()
            return render(request, 'teacher/createcourse.html', locals())


    if request.method == 'POST':
        if courserecord_id:
            courserecord = models.CourseRecord.objects.get(course_id=class_id, id=courserecord_id)
            form = forms.CourserecordForm(instance=courserecord, data=request.POST)
        else:
            form = forms.CourserecordForm(data=request.POST)
        if form.is_valid():
            if not request.POST.get('course_title'):
                form.add_error('course_title', '请输入课程标题')
                if courserecord_id:
                    return render(request, 'teacher/editcourse.html', locals())
                else:
                    return render(request, 'teacher/createcourse.html', locals())
            if request.POST.get('has_homework'):
                if not request.POST.get('homework_title'):
                    form.add_error('homework_title', '请输入作业标题')
                    if courserecord_id:
                        return render(request, 'teacher/editcourse.html', locals())
                    else:
                        return render(request, 'teacher/createcourse.html', locals())
            form.save()
            courserecord = models.CourseRecord.objects.filter(course_id=class_id, day_num=request.POST.get('day_num')).first()
            student_list = courserecord.course.customer_set.select_related()
            for student in student_list:
                models.StudyRecord.objects.get_or_create(course_record=courserecord, student=student,)
            return HttpResponseRedirect(resolve_url('courselist', class_id))
        else:
            if courserecord_id:
                return render(request, 'teacher/editcourse.html', locals())
            else:
                return render(request, 'teacher/createcourse.html', locals())


@login_required
@check_permission
def studentinformation(request):
    student_qq = request.GET.get('student_qq')
    if student_qq:
        student_item = models.Customer.objects.filter(qq=student_qq).first()
        if student_item:
            enrollments = models.Enrollment.objects.filter(customer=student_item).order_by('enrolled_date')
            if enrollments:
                enrollment_id = request.GET.get('enrollment_id')
                if not enrollment_id:
                    enrollment_id = enrollments.last().id
                if enrollment_id:
                    enrollment_id = int(enrollment_id)
                    enrollment_item = models.Enrollment.objects.filter(id=enrollment_id).first()
                    nums_class = models.StudyRecord.objects.filter(course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_100 = models.StudyRecord.objects.filter(score=100, course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_90 = models.StudyRecord.objects.filter(score=90, course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_50 = models.StudyRecord.objects.filter(score__in=[50,40], course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_0 = models.StudyRecord.objects.filter(score__in=[0,-100], course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_checked = models.StudyRecord.objects.filter(record='checked', course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_late = models.StudyRecord.objects.filter(record='late', course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_noshow = models.StudyRecord.objects.filter(record='noshow', course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    nums_leave_early = models.StudyRecord.objects.filter(record='leave_early', course_record__course=enrollment_item.course_grade, student__qq=student_qq).count()
                    punishments = models.StuPunishmentRecord.objects.filter(enrollment_id=enrollment_id)
                    study_consult_record = models.StudyConsultRecord.objects.filter(enrollment_id=enrollment_id).order_by('-date')
                status = 'True'
            else:
                status = 'False'
                error_information = '该学员没有报名任何课程，没有学习信息'
        else:
            status = 'False'
            error_information = '不存在该QQ对应的学生信息'
    else:
        status = 'False'
    return render(request, 'teacher/studentinformation.html', locals())


@login_required
@check_permission
def study_consult_record(request, enrollment_id):
    enrollment = models.Enrollment.objects.get(id=enrollment_id)
    if request.method == 'POST':
        form = forms.AddStudyConsultRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url('studentinformation') + '?student_qq=' + str(enrollment.customer.qq) + '&enrollment_id=' + str(enrollment_id))
        else:
            form = forms.AddStudyConsultRecordForm(request.POST, instance=enrollment)
            return render(request, 'crm/consult_record.html', {
                'form': form
            })
    form = forms.AddStudyConsultRecordForm(instance=enrollment)
    return render(request, 'teacher/study_consult_record.html', {
        'form': form,
    })