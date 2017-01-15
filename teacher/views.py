from django.shortcuts import render, HttpResponse, HttpResponseRedirect, resolve_url
from django.contrib.auth.decorators import login_required
from teacher import models
from teacher.permissions import check_permission
from OldboyCRM.settings import HOMEWORK_DATA_DIR
from teacher import forms
from crm import forms as crm_forms
from django.contrib.auth import login, logout, authenticate


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
def courselist(request,class_id):
    courselist = models.CourseRecord.objects.filter(course_id=class_id, course__teachers=request.user)
    return render(request, 'teacher/courselist.html', locals())


@login_required
@check_permission
def courserecord(request, course_id):
    if request.method == 'GET':
        class_id = course_id
        studyrecords = models.StudyRecord.objects.filter(course_record_id=course_id, course_record__course__teachers=request.user)
        homework_path = HOMEWORK_DATA_DIR
        return render(request, 'teacher/courserecord.html', locals())

    if request.method == 'POST':
        student_id = request.POST.get('student_id',)
        course_id = request.POST.get('course_id', )
        status = request.POST.get('status')
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
        print(form)
        for field in form:
            print(field.name)
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
            print(form.errors)
            return render(request, 'teacher/createcourse.html', locals())
