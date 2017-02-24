"""OldboyCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from  crm import urls as crm_urls
from crm import views as crm_views
from teacher import urls as teacher_urls
from student import urls as stu_urls
from OldboyCRM.settings import ENROLL_DATA_DIR


urlpatterns = [
    url(r'^stu/',include(stu_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crm/', include(crm_urls)),
    url(r'^teacher/', include(teacher_urls)),
    url(r'^$', crm_views.index ),
    url(r'^login/$', crm_views.login_url, name='login_url'),
    url(r'^enrollment_student/', crm_views.stu_enrollment, name="stu_enrollment"),
    url(r'^file_download/', crm_views.file_download, name="file_download"),
    url(r'^survery/(\d+)/', crm_views.survery, name="survery"),
    url(r'^grade/single/', crm_views.grade_check, name="single_stu_grade_check"),
    url(r'^scholarship/', crm_views.scholarship, name="scholarship"),
    url(r'^training_contract/', crm_views.training_contract, name="training_contract"),
    url(r'^compliant/', crm_views.compliant, name="compliant"),
    url(r'^stu_faq/', crm_views.stu_faq, name="stu_faq"),
    url(r'^punishment/$', crm_views.punishment, name="punishment"),
]
