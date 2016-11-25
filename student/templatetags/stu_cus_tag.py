#coding:utf-8

from django.utils.safestring import mark_safe
from django import template
register = template.Library()
from django.utils.html import escapejs, format_html
from django.shortcuts import resolve_url


from student.models import *


@register.simple_tag
def has_study(modu_id,user_qq):
    course_id = CourseModule.objects.get(id=modu_id)
    #所有的课程记录
    course_num_list = course_id.courserecord.all()
    sum_day_num = len(course_num_list)
    has_study_num = 0
    #遍历每个课程记录，筛选出该模块下 所有属于该学员的学习记录
    for every_course in course_num_list:
        try:
            studyrecord_obj = every_course.studyrecord_set.get(student__qq=user_qq)
            if studyrecord_obj.score != -1:
                has_study_num += 1
        except Exception as e:
            pass
    percent_num = str(round((has_study_num/sum_day_num)*100))+'%'
    return percent_num







