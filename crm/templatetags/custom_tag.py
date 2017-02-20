#_*_coding:utf-8_*_
__author__ = 'jieli'
import datetime
from django.utils.safestring import mark_safe
from django import template
register = template.Library()
from django.utils.html import escapejs, format_html


from crm import models

@register.filter
def get_score_color(stu_study_obj):
    return stu_study_obj.color_dic[stu_study_obj.score]

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



@register.simple_tag
def action(current_url,item,number):

    #/crm/customers_library  all  all  all  all     all.html
    # item: type name
    url_part_list = current_url.split('-')
    length = len(url_part_list)-1
    if number == length:
        if url_part_list[length] == item['type'] + '.html/1':
            temp = "<li style='background:#363c40;padding:3px 10px;float: left;margin: 5px 10px;'><a class='action_url' href='#' href_url='%s'style='color:white'>%s</a></li>"
        else:
            temp = "<li style='float: left;margin: 5px 10px;'><a class='action_url' href='#' href_url='%s'>%s</a></li>"

        url_part_list[length] = str(item['type']) + '.html/1'
    else:
        if url_part_list[number] == item['type']:
            temp = "<li style='background:#363c40;padding:0px 5px;float: left;margin: 5px 10px;'><a class='action_url' href='#' href_url='%s'style='color:white'>%s</a></li>"
        else:
            temp = "<li style='float: left;margin: 5px 10px;'><a class='action_url' href='#' href_url='%s'>%s</a></li>"

        url_part_list[number] = str(item['type'])

    ur_str = '-'.join(url_part_list)

    temp = temp % (ur_str, item['name'])

    return  mark_safe(temp)


@register.simple_tag
def action_all(current_url,index,type_name):
    # /crm/customers_library  all  all  all  all     all.html
    url_part_list = current_url.split('-')


    length=len(url_part_list)-1
    if index == length:
        url_part_list[index] = 'all.html/1'
    else:
        url_part_list[index] = 'all'
    temp = '''<a class="action_url" href='#' href_url="%s"title='取消筛选'><b>%s:</b></a>'''
    url_path = '-'.join(url_part_list)
    temp = temp %(url_path,type_name)
    return mark_safe(temp)

@register.simple_tag
def add_persent(number_no):
    cur_num=str(number_no)
    cur_num=cur_num+'%'
    return cur_num