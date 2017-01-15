#coding:utf-8

from django.core.urlresolvers import resolve
from django.shortcuts import render
from crm.permission_dict import perm_dic_teacher as perm_dic



def perm_check(*args,**kwargs):
    request = args[0]
    resolve_url_obj = resolve(request.path)
    curr_url_name = resolve_url_obj.url_name  # 当前url的url_name
    match_flag = False
    match_key = None
    for per_key,per_val in  perm_dic.items():
        per_url_name, per_meth,per_arg = per_val
        if per_url_name == curr_url_name:
            if per_meth == request.method:
                if not  per_arg:
                    match_flag = True
                    match_key = per_key
                else:       #逐个匹配参数，看每个参数时候都能对应的上。
                    for item in per_arg:
                        request_method_fun = getattr(request,request.per_meth)
                        if request_method_fun.get(item,None):# request字典中由此参数
                            match_flag = True
                        else:
                            match_flag = False
                            break  # 有一个参数不能匹配成功，则判定为假，退出该循环。

                    if match_flag == True:
                        match_key = per_key
                        break



    if match_flag:
        app_name, *per_name = match_key.split('_')
        perm_obj = '%s.%s' % (app_name,match_key)
        if request.user.has_perm(perm_obj):
            print('当前用户由此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False







def check_permission(func):
    def inner(*args,**kwargs):
        if not perm_check(*args,**kwargs):
            request = args[0]
            return render(request,'403_forbidden.html')
        return func(*args,**kwargs)
    return  inner








