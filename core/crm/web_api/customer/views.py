#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import json
import logging
from backend.commons import pager
from core.adminlte import admin
# 调用 相关的models
import copy
from core.crm.web_models.models import Customer
from core.crm.web_models import constants
from django.db.models import Q

Page_Models = Customer
Course_Constants = constants.Course_Constants
logger = logging.getLogger(__name__)


class Monitor(object):
    def __init__(self):
        self.__params = {}
        self.__adding = {}

    def add_query_param(self, k, v):
        if self.__params is None:
            self.__params = {}
        self.__params[k] = v

    def get_query_params(self):
        return self.__params

    def add_adding_param(self, k, v):
        if self.__adding is None:
            self.__adding = {}
        self.__adding[k] = v

    def get_adding_params(self):
        return self.__adding


class ClassListSearchRequest(Monitor):
    def __init__(self):
        """
        获取域名列表
        """
        Monitor.__init__(
            self
        )

    def SlKey(self):
        con = Q()
        for k, v in self.get_SlKeySearch().items():
            temp = Q()
            Kv = k.split(',')
            for i in Kv:
                temp.connector = 'OR'
                temp.children.append((i, v))
            # temp.connector = 'OR'
            # for item in v:
            #    temp.children.append((k, item))
            con.add(temp, 'AND')
        for k, v in self.get_SlKeyListFilter().items():
            k = k.split('.')[-1]
            temp = Q()
            temp.connector = 'AND'
            if v is None:
                continue
            if len(v) == 0:
                continue
            if v == '9999':
                continue
            temp.children.append((k, v))
            con.add(temp, 'AND')
        return con

    def ComPile_data(self, data):
        __data = copy.deepcopy(data)
        try:
            __data['course'] = constants.Course_Constants.get_name(__data['course'])
        except:
            pass
        try:
            __data['class_type'] = constants.Class_Type_Constants.get_name(__data['class_type'])
        except:
            pass
        try:
            __data['colored_status'] = Page_Models.objects.get(id=data['id']).colored_status()
        except:
            __data['colored_status'] = u'未知状态'
        try:
            __data['get_enrolled_course'] = Page_Models.objects.get(id=data['id']).get_enrolled_course()
        except:
            __data['get_enrolled_course'] = u'尚未发现班级'
        try:
            __data['consultant'] = Page_Models.objects.get(id=data['id']).consultant.name
        except:
            __data['consultant'] = u'尚未发现班级'
        return __data

    def do_request(self):
        """
            重构 request 方法.
            1.请求阿里云整体列表.
            2.对请求结果进行入库操作
        """
        # 验证 是否存在 SlKeyListFilter
        if self.get_SlKeyListFilter() or self.get_SlKeySearch():
            # 如果存在 多个.就继续添加即可.
            Con = self.SlKey()
            ComPile = Page_Models.objects.filter(Con)
        else:
            ComPile = Page_Models.objects.all()
        # 取出 全部内容
        ComPileData = []
        for i_data in ComPile:
            data = i_data.__dict__
            ComPileData.append(
                self.ComPile_data(data)
            )
        if type(self.get_PageNumber()) != int:
            PageNumber = int(self.get_PageNumber())
        else:
            PageNumber = self.get_PageNumber()
        if type(self.get_PageSize()) != int:
            PageSize = int(self.get_PageSize())
        else:
            PageSize = self.get_PageSize()
        try:
            page_info = pager.PageInfo(
                PageNumber,
                len(ComPileData),
                perItems=PageSize,
            )
            Projects = ComPileData[page_info.start:page_info.end]
        except Exception as e:
            logger.error(e.message, exc_info=True)
        return {
            'Projects': Projects,
            'PageSize': PageSize,
            'PageNumber': PageNumber,
            'TotalCount': len(ComPileData),
        }

    def get_PageNumber(self):
        return self.get_query_params().get('PageNumber', 1)

    def set_PageNumber(self, PageNumber):
        self.add_query_param('PageNumber', PageNumber)

    def get_PageSize(self):
        return self.get_query_params().get('PageSize', 20)

    def set_PageSize(self, PageSize):
        self.add_query_param('PageSize', PageSize)

    def get_SlKeySearch(self):
        return self.get_query_params().get('SlKeySearch', {})

    def set_SlKeySearch(self, SlKeySearch):
        self.add_query_param('SlKeySearch', SlKeySearch)

    def get_SlKeyListFilter(self):
        return self.get_query_params().get('SlKeyListFilter', {})

    def set_SlKeyListFilter(self, SlKeyListFilter):
        self.add_query_param('SlKeyListFilter', SlKeyListFilter)


class ClassListModifyRequest(Monitor):
    def __init__(self):
        """
        获取域名列表
        """
        Monitor.__init__(
            self
        )

    def get_Pk(self):
        return self.get_query_params().get('id', None)

    def set_Pk(self, Pk):
        self.add_query_param('id', Pk)

    def joining_base(self):
        """
            拼接 基础信息
        """
        if self.get_Pk() is None:
            raise Exception(u'必须拥有code值才能进行 修改')
        # 从本地中读取 code 基础信息
        BanJi = Page_Models.objects.get(id=self.get_Pk())
        DataCode = {
            'id': BanJi.id,
            "course": BanJi.course,
            "semester": BanJi.semester,
            "start_date": BanJi.start_date,
            "graduate_date": BanJi.graduate_date,
            "teachers": BanJi.teachers,
        }
        results = []
        # 拼接显示内容
        results.append(
            {
                'type': 'input',
                'code': 'id',
                'name': 'id',
                'value': DataCode['id'],
                'class': '',
                'disabled': "true",
            }
        )
        results.append(
            {
                'type': 'PositiveSmallIntegerField',
                'code': 'course',
                'name': '课程名称',
                'value': [Course_Constants.get_name(DataCode['course'])],
                'choices': Course_Constants.STATUS,
                # 'class': 'pici_1_hosts_class',
            }
        )
        results.append(
            {
                'type': 'input',
                'code': 'semester',
                'name': '学期',
                'value': DataCode['semester'],
                'class': '',
                # 'disabled': "true",
            }
        )
        results.append(
            {
                'type': 'DateField',
                'code': 'start_date',
                'name': '开班日期',
                'value': DataCode['start_date'],
                'class': '',
                # 'disabled': "true",
            }
        )
        results.append(
            {
                'type': 'DateField',
                'code': 'graduate_date',
                'name': '结业日期',
                'value': DataCode['graduate_date'],
                'class': '',
                # 'disabled': "true",
            }
        )
        # 获取讲师具体name 的方法
        __teachers_value = [
            "%s" % i.name
            for i in BanJi.teachers.all()
            ]
        __teachers_choices = [
            (i.id, i.name)
            for i in admin.models.UserProfile.objects.all()
            ]
        results.append(
            {
                'type': 'ManyToManyField',
                'code': 'teachers',
                'name': '讲师',
                'value': __teachers_value,
                'choices': __teachers_choices,
                'class': '',
                # 'disabled': "true",
            }
        )
        return results

    def joining_adding(self):
        """
            拼接附加信息
        """
        results = []
        return results

    def do_modify(self):
        """
            根据 code 获取 相关的修改信息
        """
        results = self.joining_base()
        # results += self.joining_adding()
        return results
        pass

    def do_info(self):
        """
            根据 code 获取 相关的信息
        """
        results = self.joining_base()
        # results += self.joining_adding()
        return results

    def do_post_modify(self):
        try:
            Page = Page_Models.objects.get(
                id=self.get_Pk()
            )
            Page.semester = 123
            Page.save()
        except Exception as e:
            logger.error(
                u'*' * 3 + u'post_modify' + u'*' * 3 +
                u'出现 错误. 可能是 获取不到具体内容 %s' % e.message,
                exc_info=True
            )
            raise Exception(e)
        return True


class ClassListAddDelRequest(Monitor):
    def __init__(self):
        """
        获取域名列表
        """
        Monitor.__init__(
            self
        )

    def do_request(self):
        """
            重构 request 方法.
            1.请求阿里云整体列表.
            2.对请求结果进行入库操作
        """
        # 验证 是否存在 SlKeyListFilter
        pass

    def get_Code(self):
        return self.get_query_params().get('code', None)

    def set_Code(self, Code):
        self.add_query_param('code', Code)

    def joining_base(self):
        """
            拼接 基础信息
        """
        if self.get_Code() is None:
            raise Exception(u'必须拥有code值才能进行 修改')
        # 从本地中读取 code 基础信息
        User = Page_Models.objects.get(id=self.get_Code())
        DataCode = {
            'id': User.id,
            'name': User.name,
            'password': User.password
        }
        results = []
        # 拼接显示内容
        results.append(
            {
                'type': 'input',
                'code': 'id',
                'name': '名称',
                'value': DataCode['id'],
                'class': '',
                'disabled': "true",
            }
        )
        results.append(
            {
                'type': 'input',
                'code': 'name',
                'name': '名称',
                'value': DataCode['name'],
                'class': '',
                'disabled': "true",
            }
        )
        results.append(
            {
                'type': 'input',
                'code': 'password',
                'name': '密码',
                'value': DataCode['password'],
                'class': '',
                # 'disabled': "true",
            }
        )
        return results

    def joining_adding(self):
        """
            拼接附加信息
        """
        if self.get_Code() is None:
            raise Exception(u'必须拥有code值才能进行 修改')
        # 查询数据库.并返回 othis
        User = Page_Models.objects.get(id=self.get_Code())
        results = []
        # 拼接显示内容
        results.append(
            {
                'type': 'ManyToManyField',
                'code': 'groups',
                'name': '用户组',
                'value': [i.name for i in User.groups.all()],
                'choices': [
                    [i.id, i.name]
                    for i in Groups_Models.objects.all()
                    ],
                'class': 'pici_1_hosts_class',
            }
        )
        # 获取 全部权限信息
        userpre_choices = {}
        for i in Resource_Models.objects.all():
            userpre_choices.setdefault(i.app_name, {})
            userpre = userpre_choices.get(i.app_name)
            userpre.setdefault('choices', [])
            __choices = userpre.get('choices')
            __choices.append(
                {
                    'id': i.id,
                    'name': i.name
                }
            )
        __userpre_choices = []
        for k, v in userpre_choices.items():
            __userpre_choices.append(
                {
                    'id': k,
                    'name': '%s 权限' % k,
                    'choices': v.get('choices', [])
                }
            )
        # 获取当前用户权限信息
        value = []
        for i in User.User_permission.resources.all():
            value.append(
                i.name
            )
        results.append(
            {
                'type': 'Screen',
                'code': 'userpre',
                'name': '权限',
                'value': value,
                'choices': __userpre_choices,
            }
        )
        return results

    def do_modify(self):
        """
            根据 code 获取 相关的修改信息
        """
        results = self.joining_base()
        results += self.joining_adding()
        return results
        pass

    def do_info(self):
        """
            根据 code 获取 相关的信息
        """
        results = self.joining_base()
        results += self.joining_adding()
        return results

    def do_post_modify(self):
        if self.get_adding_params():
            try:
                Page = Page_Models.objects.get(
                    code=self.get_Code()
                )
            except:
                Page = Page_Models.objects.create(
                    code=self.get_Code()
                )
            Page.other = json.dumps(self.get_adding_params())
            Page.save()
        return True


def get_search(request, ret):
    logger.debug(
        u'*' * 3 + u'get_search' + u'*' * 3 +
        u'获取模式为 Users 开始'
    )
    Req = ClassListSearchRequest()
    PageNumber = request.POST.get(u'PageNumber', None)
    if PageNumber is not None:
        Req.set_PageNumber(PageNumber)
    PageSize = request.POST.get(u'PageSize', None)
    if PageSize is not None:
        Req.set_PageSize(PageSize)
    SlKeyListFilter = request.POST.get(u'SlKeyListFilter', None)
    if SlKeyListFilter is not None:
        Req.set_SlKeyListFilter(json.loads(SlKeyListFilter))
    SlKeySearch = request.POST.get(u'SlKeySearch', None)
    if SlKeySearch is not None:
        Req.set_SlKeySearch(json.loads(SlKeySearch))
    try:
        Req = Req.do_request()
        ret['results'] = Req['Projects']
        ret["PageSize"] = Req['PageSize']
        ret["PageNumber"] = Req['PageNumber']
        ret["ret_count"] = Req['TotalCount']
        ret['per_page'] = 20
        ret['ret_code'] = 0
    except Exception as e:
        logger.error(
            u'*' * 3 + u'get_codes_data' + u'*' * 3 +
            u'%s' % e.message
        )
        ret['message'] = e.message
    logger.debug(
        u'*' * 3 + u'get_search' + u'*' * 3 +
        u'获取模式为 Users 结束'
    )
    return ret


def get_modify(request, ret):
    logger.debug(
        u'*' * 3 + u'get_modify' + u'*' * 3 +
        u'获取修改相关信息 开始'
    )
    Req = ClassListModifyRequest()
    PK = request.POST.get(u'pk', None)
    if PK is not None:
        Req.set_Pk(PK)
    try:
        ret['results'] = Req.do_modify()
        ret['ret_code'] = 0
    except Exception as e:
        ret['message'] = e.message
    logger.debug(
        u'*' * 3 + u'get_modify' + u'*' * 3 +
        u'获取修改相关信息 结束'
    )
    return ret


def post_modify(request, ret):
    logger.debug(
        u'*' * 3 + u'post_modify' + u'*' * 3 +
        u'获取相关信息 开始'
    )
    aliyun = ClassListModifyRequest()
    code = request.POST.get(u'id_id', None)
    if code is not None:
        aliyun.set_Pk(code)
    try:
        if aliyun.do_post_modify():
            ret['ret_code'] = 0
            ret['message'] = u'成功'
            ret['results'] = ''
    except Exception as e:
        ret['message'] = e.message
    logger.debug(
        u'*' * 3 + u'get_info' + u'*' * 3 +
        u'获取相关信息 结束'
    )
    return ret


def get_info(request, ret):
    logger.debug(
        u'*' * 3 + u'get_info' + u'*' * 3 +
        u'获取相关信息 开始'
    )
    Req = ClassListModifyRequest()
    PK = request.POST.get(u'pk', None)
    if PK is not None:
        Req.set_Pk(PK)
    try:
        ret['results'] = Req.do_info()
        ret['ret_code'] = 0
    except Exception as e:
        ret['message'] = e.message
    logger.debug(
        u'*' * 3 + u'get_info' + u'*' * 3 +
        u'获取相关信息 结束'
    )
    return ret


def main():
    pass


if __name__ == '__main__':
    main()
