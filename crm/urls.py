#_*_encoding:utf-8_*_

from django.conf.urls import include, url
from crm import views


urlpatterns = [
    url(r'^$', views.dashboard, name='crm_dashboard'),  # 销售基页
    url(r'^survery/(\d+)/', views.survery, name="survery"),
    url(r'^survery/report/(\d+)/', views.survery_report, name="survery_report"),
    url(r'^survery/report/chart/(\d+)/', views.survery_chart_report, name="survery_chart_report"),
    url(r'^grade/(\d+)/', views.view_class_grade, name="class_grade"),
    url(r'^grade/single/', views.grade_check, name="single_stu_grade_check"),
    url(r'^scholarship/', views.scholarship, name="scholarship"),
    url(r'^compliant/', views.compliant, name="compliant"),
    url(r'^stu_faq/', views.stu_faq, name="stu_faq"),
    url(r'^stu_lack_check_records/', views.stu_lack_check_records, name="stu_lack_check_records"),
    url(r'^grade_chart/(\d+)/', views.get_grade_chart, name="get_grade_chart"),
    url(r'^enrollment_student/', views.stu_enrollment, name="stu_enrollment"),
    url(r'^training_contract/', views.training_contract, name="training_contract"),
    url(r'^file_download/', views.file_download, name="file_download"),
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
    url(r'^login/$', views.my_login, name='my_login'),
    url(r'^logout/$', views.my_logout, name='my_logout'),
    url(r'^error/$', views.error, name='error'),
    url(r'^customer_detail/(?P<id>\d+)/$', views.customer_detail, name='customer_detail'),
    url(r'^class_list/$', views.class_list, name='class_list'),
    url(r'^class_detail-(?P<id>\d+)-(?P<status>\S+)-(?P<consultant__email>\S+).html/(?P<page>\d*)', views.class_detail,
        name='class_detail'),
    url(r'^statistical/$', views.Statistical, name='statistical'),
    url(r'^searchcustomer', views.searchcustomer, name='searchcustomer'),
    url(r'^enrollment/(?P<customer_id>\d+)/$', views.enrollment, name='enrollment'),
    url(r'^payment/(?P<payment_id>\d+)/$', views.payment, name='payment'),
]
