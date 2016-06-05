# _*_coding:utf-8_*_
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views
from .classlist import views as classlist_views

urlpatterns = [

]
urlpatterns += [
    url(r'^crm_classlist/$',
        login_required(classlist_views.Views.as_view()),
        name='classlist'
        ),  # 班级列表
]