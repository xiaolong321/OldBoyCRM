from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from teacher import models


# Create your views here.


@login_required()
def dashboard(request):
    return render(request, 'teacher/dashboard.html')


def classlist(request):
    classlists = models.ClassList.objects.filter(teachers=request.user)
    return render(request, 'teacher/classlist.html', locals())


def courselist(request,class_id):
    courselist = models.CourseRecord.objects.filter(course_id=class_id)
    print(courselist)
    return render(request, 'teacher/courselist.html', locals())


@login_required()
def rollcall(request,class_id):
    if request.method == 'GET':
        courses = models.CourseRecord.objects.filter(course_id=class_id)
        students = models.Customer.objects.filter(enrollment__course_grade_id=class_id)
        stories = models.StudyRecord.objects.filter(course_record__course_id=class_id)
        return render(request, 'teacher/rollcall.html', locals())
    if request.method == 'POST':
        student_id = request.POST.get('student_id',)
        course_id = request.POST.get('course_id', )
        status = request.POST.get('status')
        obj = models.StudyRecord.objects.filter(course_record_id=course_id, student_id=student_id)
        if obj:
            obj.update(record=status)
        else:
            models.StudyRecord.objects.create(course_record_id=course_id, student_id=student_id, record=status)
        return HttpResponse('OK')


def courserecord(request,course_id):
    if request.method == 'GET':
        courserecords = models.StudyRecord.objects.filter(course_record_id=course_id)
        print(courserecords)
        return render(request, 'teacher/courserecord.html', locals())

    if request.method == 'POST':
        student_id = request.POST.get('student_id',)
        course_id = request.POST.get('course_id', )
        status = request.POST.get('status')
        information = request.POST.get('information')
        print(student_id, course_id, status, information)
        obj = models.StudyRecord.objects.filter(course_record_id=course_id, student_id=student_id)
        print(1,obj)
        if obj:
            print(2)
            up_dict = {status:information}
            print(4,up_dict)
            obj.update(**up_dict)
            print(5,obj)
        else:
            print(3)
            create_dict ={
                'course_record_id':course_id,
                'student_id':student_id,
                status:information,
            }
            models.StudyRecord.objects.create(**create_dict)
        return HttpResponse('OK')

def createcourse(request, class_id):
    if request.method == 'GET':
        classinformation = models.CourseRecord.objects.filter(course_id=class_id).last()
        classinformation.day_num += 1
        return render(request, 'teacher/createcourse.html', locals())
    if request.method == 'POST':
        class_id = request.POST.get('class_id', )
        teacher_id = request.POST.get('teacher_id', )
        day_num = request.POST.get('day_num', )
        has_homework = request.POST.get('has_homework', )
        print(class_id, teacher_id, day_num, has_homework)
        create_dict={
            'course_id':class_id,
            'teacher_id':teacher_id,
            'day_num':day_num,
        }
        if has_homework == '1':
            create_dict['has_homework'] = True
        if has_homework == '0':
            create_dict['has_homework'] = False
        print(create_dict)
        models.CourseRecord.objects.create(**create_dict)
        new_course = models.CourseRecord.objects.filter(**create_dict).first()
        print(11111,new_course)
        obj = models.Customer.objects.filter(enrollment__course_grade_id=class_id)
        print(obj)
        for i in obj:
            models.StudyRecord.objects.create(student=i,course_record=new_course)
        return HttpResponse('OK')