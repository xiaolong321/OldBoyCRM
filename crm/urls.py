#_*_encoding:utf-8_*_

from django.conf.urls import include, url
from crm import views



urlpatterns = [
    url(r'^$', views.dashboard, name='crm_dashboard'),  # 销售基页
    url(r'^survery/report/(\d+)/', views.survery_report, name="survery_report"),
    url(r'^survery/report/chart/(\d+)/', views.survery_chart_report, name="survery_chart_report"),
    url(r'^grade/(\d+)/', views.view_class_grade, name="class_grade"),
    url(r'^stu_lack_check_records/', views.stu_lack_check_records, name="stu_lack_check_records"),
    url(r'^grade_chart/(\d+)/', views.get_grade_chart, name="get_grade_chart"),
    url(r'^tracking-(?P<source>\S+)-(?P<course>\S+)-(?P<class_type>\S+)-(?P<status>\S+)-(?P<filter_date>\S+)-(?P<consultant__email>\S+).html/(?P<page>\d*)',
        views.tracking, name='tracking'),  # 跟踪用户
    url(
        r'^signed-(?P<source>\S+)-(?P<course>\S+)-(?P<class_type>\S+)-(?P<status>\S+)-(?P<filter_date>\S+)-(?P<consultant__email>\S+).html/(?P<page>\d*)',
        views.signed, name='signed'),  # 已签约客户
    url(
        r'^customers_library-(?P<source>\S+)-(?P<course>\S+)-(?P<class_type>\S+)-(?P<status>\S+)-(?P<filter_date>\S+)-(?P<consultant__email>\S+).html/(?P<page>\d*)',
        views.customers_library, name='customers_library'),
    # 客户库
    url(r'^sale_table/$', views.sale_table, name='sale_table'),  # dashboard表销售直方图
    url(r'^addcustomer/$', views.addcustomer, name='addcustomer'),
    url(r'^addcustomer/(?P<referralfromid>\d+)/$', views.addcustomer, name='addcustomer'),
    url(r'^cus_enroll/(?P<id>\d+)/$', views.cus_enroll, name='cus_enroll'),
    url(r'^enroll_done/(?P<customer_qq>\w+)/$', views.enroll_done, name='enroll_done'),
    url(r'^consult_record/(?P<id>\d+)/$', views.consult_record, name='consult_record'),
    url(r'^login/$', views.my_login, name='CRM_my_login'),
    url(r'^logout/$', views.my_logout, name='CRM_my_logout'),
    url(r'^error/$', views.error, name='error'),
    url(r'^customer_detail/(?P<id>\d+)/$', views.customer_detail, name='customer_detail'),
    url(r'^class_list/$', views.class_list, name='class_list'),
    url(r'^class_detail-(?P<id>\d+)-(?P<status>\S+)-(?P<consultant__email>\S+).html/(?P<page>\d*)', views.class_detail,
        name='class_detail'),
    url(r'^statistical/$', views.Statistical, name='statistical'),
    url(r'^searchcustomer', views.searchcustomer, name='searchcustomer'),
    url(r'^enrollment/(?P<customer_id>\d+)/$', views.enrollment, name='enrollment'),
    url(r'^payment/(?P<payment_id>\d+)/$', views.payment, name='payment'),
    url(r'^showchannels/$', views.showchannels, name='showchannels'),
    url(r'^addchannel/$', views.addchannel, name='addchannel'),
    url(r'^addlinkman/$', views.addlinkman, name='addlinkman'),
    url(r'^addprogress/$', views.addprogress, name='addprogress'),
    url(r'^channel_detail/(?P<channel_id>\d+)/$', views.channel_detail, name='channel_detail'),
    url(r'^linkman_detail/(?P<linkman_id>\d+)/$', views.linkman_detail, name='linkman_detail'),
    url(r'^progress_detail/(?P<progress_id>\d+)/$', views.progress_detail, name='progress_detail'),
]
