# !/usr/bin/env python3
# -*- coding:utf-8 -*-


from django import template
from django.utils.safestring import mark_safe
import os

register = template.Library()


@register.simple_tag
def homework_download_button(homework_path, course_id, day_num, student_id=None):
    course_id = str(course_id)
    day_num = str(day_num)
    if student_id:
        student_id = str(student_id)
        file_path = homework_path + '/' + course_id + '/' + day_num + '/' + student_id
        buttoncontent = '作业下载'
        if os.path.exists(file_path):
            if not os.listdir(file_path):
                result = "<button class='btn'>未交作业</button>"
            else:
                result = "<a href=/file_download/?file_path={}><button class='btn btn-info'>{}</button></a>".format(file_path,buttoncontent)
        else:
            result = "<button class='btn'>未交作业</button>"
    else:
        file_path = homework_path + '/' + course_id + '/' + day_num
        buttoncontent = '全班作业下载'
        if os.path.exists(file_path):
            # result = "<a href=/file_download/?file_path={}><button class='homework_download btn btn-info'>{}</button></a>".format(file_path,buttoncontent)
            result = "<button class='homework_download btn btn-info' homework_path='{}'>{}</button>".format(file_path, buttoncontent)
        else:
            result = "<button class='btn'>未交作业</button>"
    return mark_safe(result)
