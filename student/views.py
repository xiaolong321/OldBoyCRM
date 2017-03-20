# coding:utf-8

from __future__ import absolute_import, unicode_literals
import json, os, zipfile, hashlib
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, resolve_url
from django.http import HttpResponseForbidden
from django.http import HttpResponse, FileResponse
from student import forms
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from student import models
from OldboyCRM import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from crm import models as crmmodels
from django.utils.encoding import smart_str
import time
from student.tasks import uploadhomework
import shutil
from common.message import message



#装饰器 验证用户登录
def cus_login_required(func, loginurl='/stu/', redirect_key='next'):
    def inner(request, *args, **kwargs):
        user_tr = request.session.get('username', None)
        if user_tr is None:
            return HttpResponseRedirect(loginurl + '?' + redirect_key + '=' + request.path)
        else:
            create_all_studyrecord(request, *args, **kwargs)
            return func(request, *args, **kwargs)
    return inner


#装饰器 验证用户密码是否已经修改
def change_pwd(func, chpwd_url='/stu/changepwd/', redirect_key='next'):
    def inner(request, *args, **kwargs):
        user_tr = request.session.get('username', None)
        if user_tr != None:
            user_pwd =  models.StuAccount.objects.get(stu_name__qq=user_tr).stu_pwd
            if user_pwd == hashstr(user_tr):
                return HttpResponseRedirect(chpwd_url)
            else:
                return func(request,*args,**kwargs)
    return inner


#创建学生学习记录
def create_all_studyrecord(request,*args,**kwargs):
    the_stu_qq = request.session['username']
    which_user = crmmodels.Customer.objects.get(qq=the_stu_qq)
    classes_list = which_user.class_list.all() #可能有多个记录
    for every_class in classes_list:
        #每一个班 有多少课程（）
        coursereord_list = every_class.courserecord_set.all()
        #遍历每一个课程（第几天）
        for every_course in coursereord_list:
            study_exist = crmmodels.StudyRecord.objects.filter(course_record=every_course,student=which_user).count()
            if study_exist>0:
                continue
            studyrecord = crmmodels.StudyRecord.objects.create(course_record=every_course,student=which_user)
            studyrecord.save()
    return True


def hashstr(inputstr):
    import hashlib
    inputstr=inputstr.encode()
    m = hashlib.md5()
    m.update(inputstr)
    resu = m.hexdigest()
    return resu


def stu_login(request):
    error=''
    if request.method == 'POST':
        error = '用户名或密码不正确'
        form = forms.StulogForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            username = cd['stu_name']
            password = cd['stu_pwd']
            num = models.StuAccount.objects.filter(stu_name__qq=username).count()
            if num>1:
                error = '查找到多个用户，请联系管理员'
                return render(request, 'stu/login.html', {'form': form, 'error': error})
            try:
                the_user = models.StuAccount.objects.get(stu_name__qq=username)
            except ObjectDoesNotExist as e:
                return render(request, 'stu/login.html', {'form': form, 'error': error})
            the_use_pwd = the_user.stu_pwd
            password_hash = hashstr(password)
            if the_use_pwd == password_hash:
                request.session['username']=username
                request.session['password']=password
                result= request.GET.get('next',resolve_url('myclass'))
                return HttpResponseRedirect(result)
            else:
                return render(request, 'stu/login.html', {'form': form, 'error': error})
        else:
            return render(request, 'stu/login.html', {'form': form, 'error': error})
    else:
        form = forms.StulogForm()

        return render(request,'stu/login.html',{'form':form,'error':error})


@cus_login_required
@change_pwd
def Mycourse(request,*args,**kwargs):
    username = request.session.get('username',None)
    stu_obj = models.Customer.objects.get(qq=username)
    #学员报的班级
    my_classlist = stu_obj.class_list.all()
    #遍历每一个班，看它有几个模块：
    #{班：{模块名:[课数，已学习}}
    all_data = {}
    for every_class in my_classlist:
        every_class_list=[]
        all_data[every_class]=every_class_list
        module_list = every_class.coursemodule.all()
    return render(request, 'stu/index.html', {'my_classlist':my_classlist})


@cus_login_required
@change_pwd
def Myclass(request):
    username = request.session.get('username', None)
    stu_obj = models.Customer.objects.get(qq=username)
    my_classlist = stu_obj.class_list.all()
    return render(request, 'stu/myclass.html', {'my_classlist':my_classlist})


@cus_login_required
@change_pwd
def class_detail(request, class_id):
    username = request.session.get('username', None)
    stu_obj = models.Customer.objects.get(qq=username)
    myclass = crmmodels.ClassList.objects.filter(id=class_id)
    study_records = crmmodels.StudyRecord.objects.filter(course_record__course=myclass, student_id=stu_obj.id)
    # course_records = crmmodels.CourseRecord.objects.filter(course=myclass)
    # for course_record in course_records:
    #     study_record = crmmodels.StudyRecord.objects.filter(course_record = course_record, student_id=stu_obj.id)
    #     course_record.study_record = study_record
    # for course_record in course_records:
    #     print(course_record.study_record.score)
    return render(request, 'stu/class_detail.html', {'myclass': myclass,
                                                     'study_records': study_records,})


def get_uploaded_fileinfo(file_dic,upload_dir):
    for filename in os.listdir(upload_dir):
        abs_file = '%s/%s' % (upload_dir, filename)
        file_create_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.gmtime(os.path.getctime(abs_file)))
        file_dic['files'][filename] = {'size': os.path.getsize(abs_file) / 1000,
                                           'ctime': file_create_time}


def delete_file(request, class_id, day_num):
    response = {}
    if request.method == "POST":
        username = request.session.get('username')
        student = models.Customer.objects.get(qq=username)
        course_record = crmmodels.CourseRecord.objects.filter(course_id=class_id, day_num=day_num).first()
        upload_path = "%s/%s/%s/%s" % (settings.HOMEWORK_DATA_DIR, class_id, day_num, student.id)
        filename = request.POST.get('filename')
        file_abs = "%s/%s" %(upload_path, filename.strip())
        if os.path.isfile(file_abs):
            shutil.rmtree(os.path.dirname(file_abs))
            response['msg'] = "file '%s' got deleted " % filename
        else:
            response["error"] = "file '%s' does not exist on server"% filename
    else:
        response['error'] = "only supoort POST method..."
    return HttpResponse(json.dumps(response))


@cus_login_required
@change_pwd
def homework(request, class_id, day_num):
    class_id = class_id
    day_num = day_num
    username = request.session.get('username')
    student = models.Customer.objects.get(qq=username)
    course_record = crmmodels.CourseRecord.objects.filter(course_id=class_id, day_num=day_num).first()
    if not course_record.has_homework:
        return HttpResponse(json.dumps('本节课没有布置作业'))
    else:
        upload_path = "%s/%s/%s/%s" % (settings.HOMEWORK_DATA_DIR, class_id, day_num, student.id)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
    response_dic = {'files': {}}
    if request.method == 'POST':
        if request.FILES:
            if request.FILES['file'].name.endswith('.zip'):
                if len(os.listdir(upload_path)) < 1:
                    if request.FILES['file'].size <= 5 * 1024 * 1024:
                        abs_filepath = "%s/%s" % (upload_path, '%s.zip' % student.name)
                        with open(abs_filepath, 'wb') as f:
                            for chunk in request.FILES['file'].chunks():
                                f.write(chunk)
                        customer_file_path = "%s/%s/%s" % (settings.HOMEWORK_DATA_DIR, class_id, day_num,)
                        if not course_record.course.class_type == 'pick_up_study':
                            if os.path.exists(os.path.join(customer_file_path, 'all', student.name)):
                                shutil.rmtree(os.path.join(customer_file_path, 'all', student.name))
                            for dirpath, dirnames, filenames in os.walk(upload_path):
                                for file in filenames:
                                    f = zipfile.ZipFile(os.path.join(dirpath, file), 'r',)
                                    for file_obj in f.namelist():
                                        unzipfile = f.extract(file_obj, os.path.join(customer_file_path, 'all',
                                                                                     file.split('.zip')[0]))
                            for dirpath, dirnames, filenames in os.walk(os.path.join(customer_file_path, 'all'),topdown=False, followlinks=True):
                                for item in dirnames:
                                    try:
                                        new_name = item.encode('cp437')
                                        new_name = new_name.decode('gbk')
                                        os.rename(os.path.join(dirpath,item),(os.path.join(dirpath, new_name)))
                                    except Exception:
                                        pass
                                for item in filenames:
                                    try:
                                        new_name = item.encode('cp437')
                                        new_name = new_name.decode('gbk')
                                        os.rename(os.path.join(dirpath, item),(os.path.join(dirpath, new_name)))
                                    except Exception:
                                        pass
                        else:
                            pick_learn = crmmodels.OnlineStuAssignment.objects.filter(enrollment__customer=student, enrollment__course_grade=course_record.course).first()
                            object = message(subject='homework_upload', toaddrs=[pick_learn.assistant.name.email])
                            object.getcontent(assistantname=pick_learn.assistant.name,
                                              classname=pick_learn.enrollment.course_grade.course,
                                              studentname=student.name, studentqq=student.qq,
                                              classid=pick_learn.enrollment.course_grade.id,
                                              studentid=student.id,
                                              )
                            object.sendmessage()

                        # uploadhomework.delay(class_id, day_num, upload_path)
                    else:
                        return HttpResponseForbidden('只允许上传大小小于5M的文件')
                else:
                    return HttpResponseForbidden('只允许上传一个文件')
            else:
                return HttpResponseForbidden('只允许上传.zip格式的文件')
            get_uploaded_fileinfo(response_dic, upload_path)
            return HttpResponse(json.dumps(response_dic))
    else:
        get_uploaded_fileinfo(response_dic, upload_path)
        study_record = crmmodels.StudyRecord.objects.filter(course_record=course_record, student=student).first()
        return render(request, 'stu/homework.html', {'course_record': course_record,
                                                     'study_record': study_record,
                                                     'uploaded_files': response_dic,})


def stu_logout(request):
    request.session.clear()
    return  HttpResponseRedirect(resolve_url('/'))


@cus_login_required
def changepwd(request):
    error_msg=''
    if request.method == 'POST':
        oldpwd_no = request.POST.get('oldpwd',None).strip()
        print('oldpwd',oldpwd_no)
        newpwd1_no = request.POST.get('newpwd1',None).strip()
        print('newpwd ',newpwd1_no,len(newpwd1_no))
        newpwd2_no = request.POST.get('newpwd2',None).strip()
        if oldpwd_no and newpwd1_no and newpwd2_no:
            oldpwd = hashstr(oldpwd_no)
            newpwd1 = hashstr(newpwd1_no)
            newpwd2 = hashstr(newpwd2_no)
            form = forms.ChangepwdForm(request.POST)
            if form.is_valid():
                the_cur_qq = request.session['username']
                the_user = models.StuAccount.objects.get(stu_name__qq=the_cur_qq)
                if the_user:
                    the_oldpwd = the_user.stu_pwd
                    if oldpwd == the_oldpwd:
                        if oldpwd != newpwd2:
                            if newpwd1 == newpwd2:
                                the_user.stu_pwd=newpwd1
                                the_user.save()
                                return HttpResponseRedirect(resolve_url('stu_logout'))
                            else:
                                error_msg = '两次输入的新密码要一致'
                        else:
                            error_msg = '新旧密码不能一样'
                    else:
                        error_msg='原密码不正确'
                else:
                    print('该用户不存在')

            else:
                pass
        else:
            error_msg = '密码不能为空'
            # return render(request, 'stu/changepwd.html', {'form': form,'error_msg':error_msg})


    form = forms.ChangepwdForm()
    return render(request,'stu/changepwd.html',{'form':form,'error_msg':error_msg})


@cus_login_required
@change_pwd
def module_detail(request, *args, **kwargs):
    # 此页面为模块细节页面  主要展示 该模块下有哪些 课程  （第几周课）
    # 通过 id 获取该 module 对象
    id = request.GET.get('id')
    id = int(id)
    the_module = models.CourseModule.objects.get(id=id)

    # 通过 课程 的外键，查找属于该模块的所有 课程  CourseRecord 表
    all_classes = the_module.courserecord.all()
    #生成一个嵌套的列表[ 第几周，课程内容，作业描述，成绩，备注，作业文件,提交作业（哪个班级，哪个学期，第几天）]
    #  CourseRecord表的字段：第几周，课程内容，作业描述
    # 通过每个CourseRecord 反向外键查询 StudyRecord表获取部分字段
    # 属于StudyRecord: 成绩、备注（教师），该表需要获取当前用户 和 当前课程名字和天数 来限定查询
    #
    #获取当前
    curr_user_qq = request.session['username']
    datas = []  # 处理所有的课程信息，用于返回前端
    for  every_class in all_classes: #该模块下的所有课程
        the_class=[]  # 每个课程表创建一个空的列表用装上述内容
        the_class.extend([
            every_class.day_num,   #i.0  第几天
            every_class.course_memo,  #i.1  课程内容
            every_class.homework_memo, #i.2 作业描述
            every_class.course.course,      #i.3 哪个班级
            every_class.course.semester,     #i.4  哪个学期
            ])
        # 获取所有属于该 课程的成绩，限定用户
        try:
            the_user_sturec = every_class.studyrecord_set.get(student__qq = curr_user_qq)
        except ObjectDoesNotExist  as e:
            the_user_sturec = None
        if the_user_sturec:
            for item in crmmodels.StudyRecord.score_choices:
                if item[0] == the_user_sturec.score:
                  human_score = item[1]

            if the_user_sturec.homework:
                the_class.extend([
                    human_score,   #i.5  分数
                    the_user_sturec.note,    #i.6  教师备注
                    the_user_sturec.homework])  #i.7  学生作业文件
            else:
                the_class.extend([
                    human_score,
                    the_user_sturec.note,
                    '--'])

        else:
            the_class.extend(['N/A','--'])
        datas.append(the_class)

    return  render(request,'stu/module_detail.html',{'datas':datas,'the_module':the_module})


@cus_login_required
@change_pwd
def uploadfile(request,clas,sem,day):
    #存储目录为     # g:/oldboy/OldBoyCRM/stu_code/ LinuxL1/1/1/231567452  根目录/课程/学期/第几天/qq号
    *throw,which_class,which_semester,which_day = request.path.split('/')
    which_user = request.session['username']
    file_path = ('%s/%s/%s/%s/%s/' % (settings.UPLOADCODE_DIR, which_class, which_semester, which_day,which_user)).replace('\\', '/')

    files_size = {}
    error = ''
    form = forms.StudyrecordForm()
    #判断学员是否已经有成绩,如果已经有了，那么跳出该页
    try:
        studyrecord_obj = models.StudyRecord.objects.get(
                    course_record__course__course=which_class,
                    course_record__course__semester=which_semester,
                    course_record__day_num = which_day,
                    student__qq = which_user)
    except ObjectDoesNotExist as e:
        studyrecord_obj = None
    else:
        if studyrecord_obj.score != -1:
            return HttpResponseRedirect(resolve_url('mycourse'))

    if request.method == 'POST':
        # 获取用户输入及文件
        stu_memo = request.POST.get('stu_memo',None)
        code_file = request.FILES.get('homework',None)
        form = forms.StudyrecordForm(request.POST)
        #检测文件是否上传
        if code_file != None:
            #多次上传文件不得超过5M
            max_upload = 1024 * 1024 * 5
            if code_file.size < max_upload:
                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                file_all_path = os.path.join(file_path,code_file.name)
                #已上传文件大小之和
                have_upload_size = 0

                #遍历已上传文件，计算其和，使其小于 5M
                inner_file = os.listdir(file_path)
                for item in inner_file:
                    item_path = os.path.join(file_path,item)
                    have_upload_size += os.path.getsize(item_path)

                if (have_upload_size+code_file.size) < max_upload:
                    with open(file_all_path,'wb') as upload_file_obj:
                        #如果大于 64K 分片上传
                        if code_file.multiple_chunks():
                            for chunk in code_file.chunks():
                                upload_file_obj.write(chunk)
                        else:
                            upload_file_obj.write(code_file.read())
                    # 查看该学习记录是否存在，否则就创建一个新的
                    which_day = int(which_day)
                    which_semester = int(which_semester)
                    the_course_obj = models.CourseRecord.objects.get(
                        course__course=which_class,
                        course__semester=which_semester,
                        day_num=which_day)
                    the_student_obj = models.Customer.objects.get(qq=which_user)
                    try:
                        the_studyrecord = models.StudyRecord.objects.get(
                                                student=the_student_obj,
                                                course_record=the_course_obj)

                    except ObjectDoesNotExist:
                        the_studyrecord = models.StudyRecord(
                                            course_record=the_course_obj,
                                            student=the_student_obj)
                        the_studyrecord.save()
                    if stu_memo:
                        the_studyrecord.stu_memo = stu_memo
                        the_studyrecord.save()

                else:
                    error = '所有上传文件大小之和不能超过 5M,请删除已有文件之后再上传'
            else:
                error='单个文件大小不能超过 5M'
        else:
            error ='请选择上传文件'

    #以下为get访问部分

    if os.path.exists(file_path):
        inner_file = os.listdir(file_path)
        sum_upload_size = 0

        for item in inner_file:

            item_path = os.path.join(file_path,item)
            file_size = os.path.getsize(item_path)
            files_size[item] = file_size
            sum_upload_size +=file_size

        if inner_file:
            files_size['合计'] = sum_upload_size
    else:
        print('该目录不存在')

    return render(request,'stu/upload.html',{'form':form,'files_size':files_size,'error':error})


@cus_login_required
@change_pwd
def Myhomework(request):
    which_user_qq = request.session['username']
    which_user_obj = models.Customer.objects.get(qq=which_user_qq)
    which_classes = which_user_obj.class_list.all()
    #遍历每一个班，返回一个列表 [ 班名，第几天，成绩，代码]
    all_data_list = {}


    #遍历该学生报名的每一个班
    for every_class in which_classes:
        which_course = every_class.course
        which_semester = every_class.semester
        for item in crmmodels.course_choices:
            if item[0] == which_course:
                hunman_course = item[1]
        class_list = (which_course,hunman_course,which_semester)
        studyrecords = models.StudyRecord.objects.filter(
                        student__qq=which_user_qq,
            course_record__course__course=which_course,
            course_record__course__semester=which_semester)

        #遍历该班的属于该学生的每一个学习记录
        all_study_list =[]
        for every_study in studyrecords:
            for item_sorce in crmmodels.StudyRecord.score_choices:
                if item_sorce[0] == every_study.score:
                    hunman_score = item_sorce[1]

            the_day = every_study.course_record.day_num
            the_score = hunman_score
            the_homework = every_study.homework
            file_path = ('%s/%s/%s/%s/%s/' %
                (settings.UPLOADCODE_DIR, which_course, which_semester, the_day, which_user_qq)).replace('\\', '/')
            #遍历该学习记录下，有没有上传文件。如果有填入[]，如果没有置为‘--’
            all_file_list=[the_day,the_score]
            try:
                inner_file_list = os.listdir(file_path)
            except FileNotFoundError as e:
                inner_file_list=[]
            inner_file_str = '--'.join(inner_file_list)

            all_file_list.append(inner_file_str)
            all_study_list.append(all_file_list)
        all_data_list[class_list]=all_study_list

    #[['LinuxL1', 2, [1,80, ['flow.jpg', 'u=658211275,2221369257&fm=21&gp=0.jpg']], [3, ['flow.jpg']], [4, []], [5, []]],
     #['PythonFullStack', 2]]
    #[班级，学期，[第几节课，分数,[文件1，文件2...]]]

    return render(request,'stu/myhomework.html',{'all_data_list':all_data_list})


@cus_login_required
@change_pwd
def DeleteFile(request,*args,**kwargs):
    which_user = request.session['username']
    if request.method == 'POST':
        file_name = request.POST.get('file_name',None)
        files_path =request.POST.get('file_path',None)
        file__some_path = '/'.join(files_path.split('/')[3:])
        file_all_path = ('%s/%s/%s/' %(settings.UPLOADCODE_DIR,file__some_path,which_user)).replace('\\','/')
        the_file = os.path.join(file_all_path,file_name)
        file_exit = os.path.exists(the_file)
        if file_exit:
            os.remove(the_file)
        inner_file = os.listdir(file_all_path)
        curr_size = 0

        for file in inner_file:
            every_file_path = os.path.join(file_all_path,file)
            file_size = os.path.getsize(every_file_path)
            curr_size += file_size

        if curr_size > 0:
            if curr_size >1048576:
                size_m = curr_size/1024/1024
                size_one = round(size_m,1)
                resu = str(size_one)+' MB'
            elif curr_size> 1024:
                size_k = curr_size/1024
                size_one=round(size_k,1)
                resu = str(size_one)+' KB'
            else:
                size_b =curr_size
                size_one = round(size_b,1)
                resu = str(size_one) + ' 字节'
        else:
            resu = 0
        result = json.dumps(resu)
        return HttpResponse(result)


@cus_login_required
@change_pwd
def DownloadFile(request,*args,**kwargs):
    the_user_qq = request.session['username']
    which_class = request.GET.get('which_class',None)
    which_semester = request.GET.get('which_seme',None)
    which_day = request.GET.get('which_day',None)
    file_path = ("%s/%s/%s/%s/%s"%(
                            settings.UPLOADCODE_DIR,
                            which_class,
                            which_semester,
                            which_day,
                            the_user_qq)).replace('\\','/'),

    # 创建压缩文件名字

    file_path_parent = ("%s/%s/%s/%s" % (
                            settings.UPLOADCODE_DIR,
                            which_class,
                            which_semester,
                            which_day)).replace('\\', '/'),

    if os.path.exists(file_path):
        files = os.listdir(file_path)
        if files:
            # 创建压缩文件名字
            filename = '%s.zip' % the_user_qq
            # 创建压缩文件对象 ,类似write函数，如果该文件不存在就创建，这是个在每一天下面创建每一个学员的压缩文件。
            zipfile_obj = zipfile.ZipFile('%s/%s' % (file_path_parent, filename), 'w', zipfile.ZIP_DEFLATED)
            # 遍历目录内的每一个文件，写入压缩对象。
            for every_file in files:
                # 写入文件，（文件路径/文件名，文件名）
                zipfile_obj.write('%s/%s' % (file_path, every_file), every_file)
            zipfile_obj.close()
            # 读取压缩文件到response对象
            response = FileResponse(open('%s/%s' % (file_path_parent, filename), 'rb'))
            # 设置response告诉brower处理方式
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response['X-Sendfile'] = smart_str(file_path)
            return response

        else:
            return HttpResponseRedirect(resolve_url('myhomework'))

    else:
        return HttpResponseRedirect(resolve_url('myhomework'))


def Mycontractlist(request):
    classlist = models.ClassList.objects.filter(enrollment__customer__qq=request.session['username'])
    username = request.session['username']
    return render(request, 'stu/mycontractlist.html', locals())


def Contractdetail(request, class_id):
    customer = models.Customer.objects.filter(qq=request.session['username']).first()
    contract = models.ContractTemplate.objects.filter(classlist=class_id).first()
    return render(request, 'stu/contractdetail.html', locals())


def Myrecommendation(request):
    if request.method == 'GET':
        form = forms.ReferralForm()
    if request.method == 'POST':
        form = forms.ReferralForm(request.POST)
        if form.is_valid():
            referral_qq = request.POST.get('qq')
            customer = models.Customer.objects.filter(qq=referral_qq)
            if not customer:
                referral_from = models.StuAccount.objects.filter(id=request.POST.get('referral_from')).first()
                qq = request.POST.get('qq')
                phone = request.POST.get('phone')
                name = request.POST.get('name')
                comment = request.POST.get('comment')
                consultant = models.UserProfile.objects.filter(id=request.POST.get('consultant')).first()
                creat_dict = {
                    'referralfrom': referral_from,
                    'qq': qq,
                    'phone': phone,
                    'name': name,
                    'comment': comment,
                    'consultant': consultant,
                }
                models.Referral.objects.create(**creat_dict)
                form = forms.ReferralForm()
            else:
                form.add_error('qq', '该学生已经存在')
    recommendations = models.Referral.objects.filter(referralfrom__stu_name__qq=request.session['username'])
    for recommendation in recommendations:
        customer = models.Customer.objects.filter(qq=recommendation.qq).first()
        if customer:
            recommendation.customer = customer
            if customer.status == 'paid_in_full':
                recommendation.status = '推荐成功'
            else:
                recommendation.status = '正在沟通'
        else:
            recommendation.status = '等待沟通'
    user = models.StuAccount.objects.filter(stu_name__qq=request.session['username']).first()
    return render(request, 'stu/myrecommendation.html', locals())


def mypunishment(request):
    result = {'enrollment_records': []}
    enrollments = crmmodels.Enrollment.objects.filter(customer__qq=request.session['username'])
    for enrollment in enrollments:
        punishments = crmmodels.StuPunishmentRecord.objects.filter(enrollment=enrollment)
        counts = punishments.count()
        points = 0
        for punishment in punishments:
            points += punishment.rule.points
        result['enrollment_records'].append({'id': enrollment.id, 'course': enrollment.course_grade,
                                             'teachers': enrollment.course_grade.teachers.all(),
                                             'counts': counts, 'points': points})
    return render(request, 'stu/mypunishment.html', result)


def punishmentdetail(request,enrollment_id):
    punishments = models.StuPunishmentRecord.objects.filter(enrollment_id=enrollment_id)
    return render(request, 'stu/punishmentdetail.html', locals())