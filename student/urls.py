# coding:utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.stu_login, name='stu_login'),
    url(r'^mycourse/$', views.Mycourse, name='mycourse'),
    url(r'^myclass/$', views.Myclass, name='myclass'),
    url(r'^class_detail_student/(?P<class_id>\d+)', views.class_detail, name='class_detail_student'),
    url(r'^homework/(\d+)/(\d+)/delete/$', views.delete_file, name="delete_file"),
    url(r'^homework/(?P<class_id>\d+)/(?P<day_num>\d+)', views.homework, name='homework'),
    url(r'^mycontractlist/$', views.Mycontractlist, name='mycontractlist'),
    url(r'^contractdetail/(?P<class_id>\d+)', views.Contractdetail, name='contractdetail'),
    url(r'^myrecommendation/$', views.Myrecommendation, name='myrecommendation'),
    url(r'^module_detail/$', views.module_detail, name='module_detail'),
    url(r'^stu_logout', views.stu_logout, name='stu_logout'),
    url(r'^upload/(?P<clas>\w+)/(?P<sem>\w+)/(?P<day>\w+)', views.uploadfile, name='uploadfile'),
    url(r'^changepwd/$', views.changepwd, name='changepwd'),
    url(r'^myhomework/$', views.Myhomework, name='myhomework'),
    url(r'^delete_file/$', views.DeleteFile, name='delete_file'),
    url(r'^downloadfile/$', views.DownloadFile, name='downloadfile'),
    url(r'^mypunishment/$', views.mypunishment, name='mypunishment'),
    url(r'^punishmentdetail/(?P<enrollment_id>\d+)/$', views.punishmentdetail, name='punishmentdetail'),
]
