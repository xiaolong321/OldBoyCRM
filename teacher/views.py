from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from teacher import models
from teacher.permissions import check_permission

# Create your views here.


@login_required
@check_permission
def dashboard(request):
    return render(request, 'teacher/dashboard.html')


@login_required
@check_permission
def classlist(request):
    if request.method == 'GET':
        classlists = models.ClassList.objects.filter(teachers=request.user)
        return render(request, 'teacher/classlist.html')


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
        courserecords = models.StudyRecord.objects.filter(course_record_id=course_id, course_record__course__teachers=request.user)
        return render(request, 'teacher/courserecord.html', locals())

    if request.method == 'POST':
        student_id = request.POST.get('student_id',)
        course_id = request.POST.get('course_id', )
        status = request.POST.get('status')
        information = request.POST.get('information')
        obj = models.StudyRecord.objects.filter(course_record_id=course_id, student_id=student_id, course_recordcourse__teachers=request.user)
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
    if request.method == 'GET':
        flag = models.CourseRecord.objects.filter(course_id=class_id, course__teachers=request.user).order_by('day_num').last()
        if flag:
            classinformation = flag
            classinformation.day_num += 1
        else:
            classinformation = models.ClassList.objects.filter(id=class_id).last()
            classinformation.day_num = 1
        print(classinformation.course)
        class_id = class_id
        return render(request, 'teacher/createcourse.html', locals())
    if request.method == 'POST':
        class_id = request.POST.get('class_id', )
        teacher_id = request.POST.get('teacher_id', )
        day_num = request.POST.get('day_num', )
        has_homework = request.POST.get('has_homework', )
        create_dict={
            'course_id':class_id,
            'teacher_id':teacher_id,
            'day_num':day_num,
        }
        if has_homework == '1':
            create_dict['has_homework'] = True
        if has_homework == '0':
            create_dict['has_homework'] = False
        models.CourseRecord.objects.create(**create_dict)
        new_course = models.CourseRecord.objects.filter(**create_dict).first()
        obj = models.Customer.objects.filter(enrollment__course_grade_id=class_id)
        for i in obj:
            models.StudyRecord.objects.create(student=i,course_record=new_course)
        return HttpResponse('OK')