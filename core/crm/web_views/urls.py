# _*_coding:utf-8_*_
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views
from .courserecord import views as courserecord_views
from .paymentrecord import views as paymentrecord_views
from .studyrecord import views as studyrecord_views
from .studentfaq import views as studentfaq_views
from .compliant import views as compliant_views
from .customer import views as customer_views
from .consultrecord import views as consultrecord_views
from .classlist import views as classlist_views
from .survery import views as survery_views
from .surveryitem import views as surveryitem_views
from .surveryrecord import views as surveryrecord_views

urlpatterns = [

]
urlpatterns += [
    url(r'^crm_courserecord/$',
        login_required(courserecord_views.Views.as_view()),
        name='courserecord'
        ),  # 上课纪录
    url(r'^crm_paymentrecord/$',
        login_required(paymentrecord_views.Views.as_view()),
        name='paymentrecord'
        ),  # 交款纪录
    url(r'^crm_studyrecord/$',
        login_required(studyrecord_views.Views.as_view()),
        name='studyrecord'
        ),  # 学员学习纪录
    url(r'^crm_studentfaq/$',
        login_required(studentfaq_views.Views.as_view()),
        name='studentfaq'
        ),  # 学员常见问题汇总
    url(r'^crm_compliant/$',
        login_required(compliant_views.Views.as_view()),
        name='compliant'
        ),  # 学员投诉\建议
    url(r'^crm_customer/$',
        login_required(customer_views.Views.as_view()),
        name='customer'
        ),  # 客户信息表
    url(r'^crm_consultrecord/$',
        login_required(consultrecord_views.Views.as_view()),
        name='consultrecord'
        ),  # 客户咨询跟进记录
    url(r'^crm_classlist/$',
        login_required(classlist_views.Views.as_view()),
        name='classlist'
        ),  # 班级列表
    url(r'^crm_survery/$',
        login_required(survery_views.Views.as_view()),
        name='survery'
        ),  # 调查问卷
    url(r'^crm_surveryitem/$',
        login_required(surveryitem_views.Views.as_view()),
        name='surveryitem'
        ),  # 调查问卷问题列表
    url(r'^crm_surveryrecord/$',
        login_required(surveryrecord_views.Views.as_view()),
        name='surveryrecord'
        ),  # 问卷记录
]