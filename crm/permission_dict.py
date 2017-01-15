# coding:utf-8

# 权限样式 app_权限名字
perm_dic_CRM = {
    'crm_views_customer_detail':['customer_detail','GET',[]],
    'crm_edit_own_customer_info':['customer_detail','POST',[]],
    'crm_view_customer_enro':['cus_enroll','GET',[]],
    'crm_edit_customer_enro':['cus_enroll','POST',[]],
    'crm_view_enro_done':['enroll_done','GET',[]],
    'crm_edit_enro_done':['enroll_done','POST',[]],
    'crm_view_tracking':['tracking','GET',[]],
    'crm_view_library':['customers_library','GET',[]],
    'crm_view_signed':['signed','GET',[]],
    'crm_view_classlist':['class_list','GET',[]],
    'crm_view_statistical':['statistical','GET',[]],
    'crm_view_classdetail':['class_detail','GET',[]],
    'crm_edit_classdetail':['class_detail','POST',[]],
    'crm_view_consult_record':['consult_record','GET',[]],
    'crm_edit_consult_record':['consult_record','POST',[]],
    'crm_view_addcustomer':['addcustomer','GET',[]],
    'crm_edit_addcustomer':['addcustomer','POST',[]],
    'crm_view_dashboard':['dashboard','GET',[]],
    'crm_view_enrollment': ['enrollment', 'GET', []],
    'crm_edit_enrollment': ['enrollment', 'POST', []],
    'crm_view_payment': ['payment', 'GET', []],
    'crm_edit_payment': ['payment', 'POST', []],
}


perm_dic_teacher = {
    'teacher_view_teacher_dashboard': ['teacher_dashboard', 'GET', []],
    'teacher_view_classlist': ['classlist', 'GET', []],
    'teacher_view_courselist': ['courselist', 'GET', []],
    'teacher_view_courserecord': ['courserecord', 'GET', []],
    'teacher_edit_courserecord': ['courserecord', 'POST', []],
    'teacher_view_createcourse': ['createcourse', 'GET', []],
    'teacher_edit_createcourse': ['createcourse', 'POST', []],
}