
from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^survery/(\d+)/',views.survery,name="survery"),
    url(r'^survery/report/(\d+)/',views.survery_report,name="survery_report"),
    url(r'^survery/report/chart/(\d+)/',views.survery_chart_report,name="survery_chart_report"),
    url(r'^grade/(\d+)/',views.view_class_grade,name="class_grade"),
    url(r'^grade/single/',views.grade_check,name="single_stu_grade_check"),
    url(r'^scholarship/',views.scholarship,name="scholarship"),
    url(r'^compliant/',views.compliant,name="compliant"),
    url(r'^stu_faq/',views.stu_faq,name="stu_faq"),
    url(r'^stu_lack_check_records/',views.stu_lack_check_records,name="stu_lack_check_records"),
    url(r'^grade_chart/(\d+)/',views.get_grade_chart,name="get_grade_chart"),
]
