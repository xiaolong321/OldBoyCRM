#_*_coding:utf-8_*_
__author__ = 'jieli'
import datetime

from django import template
register = template.Library()
from django.utils.html import escapejs, format_html


from crm import models


@register.simple_tag
def load_score_list():
    html = '''<ul class="pagination">'''
    for i in range(1,11):
        html += '''<li><span style="cursor:pointer" onclick="AddScore(this)">%s</span></li>''' %(i)
    html += "</ul>"

    return format_html(html)




@register.simple_tag
def pagenator(obj,data_type):
    html = '''<ul class="pagination">'''
    if obj.has_previous():
        html += '''<li class="disabled"><a href="?page=%s&type=%s" class="fa fa-angle-double-left"></a></li>''' %(obj.previous_page_number(),data_type)


    for p_num in obj.paginator.page_range:
        if p_num == obj.number:
            html += '''<li class="active"><a href="?page=%s&type=%s">%s</a></li>''' %(p_num,data_type,p_num)
        else:
            html += '''<li ><a href="?page=%s&type=%s">%s</a></li>''' %(p_num,data_type,p_num)
    if obj.has_next():
        html += '''<li class="disabled"><a href="?page=%s&type=%s" class="fa fa-angle-double-right"></a></li>''' %( obj.next_page_number(),data_type)

    html += "</ul>"

    return html


@register.simple_tag
def valid_survery_count(obj):
    #print(obj)
    #print(obj.select_related())
    #for i in obj.select_related():
    #    print i.survery_item

    total_survery_records =   obj.surveryrecord_set.select_related().count()
    total_questions = obj.questions.select_related().count()
    #print total_survery_records
    return total_survery_records / total_questions

@register.simple_tag
def get_single_stu_total_scores(course,stu_obj):
    total_score = 0
    for eachday in course.courserecord_set.select_related():
        for stu_day_grade in eachday.studyrecord_set.select_related():
            if stu_day_grade.student.id == stu_obj.id :
                if stu_day_grade.score != -1: #-1 means N/A, no grade record for this day
                    total_score += stu_day_grade.score


    return total_score