
from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^survery/(\d+)/',views.survery,name="survery"),
    url(r'^survery/report/(\d+)/',views.survery_report,name="survery_report"),
    url(r'^survery/report/chart/(\d+)/',views.survery_chart_report,name="survery_chart_report"),
    url(r'^grade/(\d+)/',views.view_class_grade,name="class_grade"),
]
