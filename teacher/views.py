from django.shortcuts import render, HttpResponse, HttpResponseRedirect, resolve_url
from django.contrib.auth.decorators import login_required
from teacher import models
from teacher.permissions import check_permission
from OldboyCRM.settings import HOMEWORK_DATA_DIR
from teacher import forms
from crm import forms as crm_forms
from django.contrib.auth import login, logout, authenticate
import os
from crm import views as crm_views
import zipfile
from OldboyCRM import settings


# Create your views here.


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
    if class_obj.class_type == 'pick_up_study':
        student_list = models.OnlineStuAssignment.objects.filter(enrollment__course_grade=class_obj,
                                                        assistant__name__email=request.user.email)
        return render(request, 'teacher/online_student_list.html', locals())
    else:
        courselist = models.CourseRecord.objects.filter(course_id=class_id, course__teachers=request.user)
        return render(request, 'teacher/courselist.html', locals())


@login_required
@check_permission
def courserecord(request, course_id, student_id=None):
    if request.method == 'GET':

        homework_path = HOMEWORK_DATA_DIR
        if not student_id == '0':
            OnlineStuAssignment = models.OnlineStuAssignment.objects.filter(enrollment__customer_id=student_id,
                                                          enrollment__course_grade_id=course_id).first()
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
            obj = models.StudyRecord.objects.filter(course_record_id=course_id, student_id=student_id,)
            if obj:
                up_dict = {status:information}
                obj.update(**up_dict)
            else:
                create_dict ={
                    'course_record_id':course_id,
                    'student_id':student_id,
                    status:information,
                }
                models.StudyRecord.objects.create(**create_dict)
            return HttpResponse('OK')


@login_required
@check_permission
def createcourse(request, class_id):
    flag = models.CourseRecord.objects.filter(course_id=class_id, course__teachers=request.user).order_by(
        'day_num').last()
    if flag:
        day_num = flag.day_num + 1
    else:
        day_num = 1
    if request.method == 'GET':
        form = forms.CourserecordForm()
        return render(request, 'teacher/createcourse.html', locals())
    if request.method == 'POST':
        form = forms.CourserecordForm(data=request.POST)
        if form.is_valid():
            if not request.POST.get('course_title'):
                form.add_error('course_title','请输入课程标题')
                return render(request, 'teacher/createcourse.html', locals())
            if request.POST.get('has_homework'):
                if not request.POST.get('homework_title'):
                    form.add_error('homework_title', '请输入作业标题')
                    return render(request, 'teacher/createcourse.html', locals())
                else:
                    form.save()
                    return HttpResponseRedirect(resolve_url('courselist', class_id))
            else:
                form.save()
                return HttpResponseRedirect(resolve_url('courselist',class_id))
        else:
            return render(request, 'teacher/createcourse.html', locals())
