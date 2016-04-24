#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging

logger = logging.getLogger(__name__)


class Course_Constants(object):
    STATUS = (
        ('LinuxL1', u'Linux中高级'),
        ('LinuxL2', u'Linux架构师'),
        ('Linux51', u'Linux中高级(51网络)'),
        ('LinuxL251', u'Linux中高级+架构合成班(51网络)'),
        ('PythonDevOps', u'Python自动化开发'),
        ('PythonFullStack', u'Python高级全栈开发'),
        ('PythonDevOps51', u'Python自动化开发(51网络)'),
        ('PythonFullStack51', u'Python全栈开发(51网络)'),
        ('BigDataDev', u"大数据开发课程"),
        ('Cloud', u"云计算课程"),

    )

    @staticmethod
    def get_code(name):
        for i in Course_Constants.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in Course_Constants.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class Class_Type_Constants(object):
    STATUS = (
        ('online', u'网络班'),
        ('offline_weekend', u'面授班(周末)',),
        ('offline_fulltime', u'面授班(脱产)',),
    )

    @staticmethod
    def get_code(name):
        for i in Class_Type_Constants.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in Class_Type_Constants.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class Customer_Status(object):
    """
    任务状态
    """
    signed = 'signed'
    unregistered='unregistered'
    STATUS = (
        (signed, u"已报名"),
        (unregistered, u"未报名"),
        ('paid_in_full', u"学费已交齐")
    )

    @staticmethod
    def get_code(name):
        for i in Customer_Status.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in Customer_Status.STATUS:
            if str(code) == str(i[0]):
                return i[1]

class Customer_Source(object):
    """
    任务状态
    """
    QQ = 'qq'
    STATUS = (
        ('qq', u"qq群"),
        ('referral', u"内部转介绍"),
        ('51cto', u"51cto"),
        ('others', u"其它"),
    )

    @staticmethod
    def get_code(name):
        for i in Customer_Status.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in Customer_Status.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class ConsultRecord_Status(object):
    """
    任务状态
    """
    STATUS = (
        (1, u"近期无报名计划"),
        (2, u"2个月内报名"),
        (3, u"1个月内报名"),
        (4, u"2周内报名"),
        (5, u"1周内报名"),
        (6, u"2天内报名"),
        (7, u"已报名"),
        (8, u"已交全款"),
    )

    @staticmethod
    def get_code(name):
        for i in ConsultRecord_Status.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in ConsultRecord_Status.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class PaymentRecord_pay_type(object):
    deposit = 'deposit'
    STATUS = (
        (deposit, u"订金/报名费"),
        ('tution', u"学费"),
        ('refund', u"退款"),
    )

    @staticmethod
    def get_code(name):
        for i in PaymentRecord_pay_type.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in PaymentRecord_pay_type.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class StudyRecord_record(object):
    checked = 'checked'
    STATUS = (
        (checked, u"已签到"),
        ('late', u"迟到"),
        ('noshow', u"缺勤"),
        ('leave_early', u"早退"),
    )

    @staticmethod
    def get_code(name):
        for i in StudyRecord_record.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in StudyRecord_record.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class StudyRecord_score(object):
    N_A = '-1'
    color_dic = {
        100: "#5DFC70",
        90: "yellowgreen",
        85: "deepskyblue",
        80: "#49E3F5",
        70: "#1CD4C8",
        60: "#FFBF00",
        50: "#FF8000",
        40: "#FE642E",
        0: "red",
        -1: "#E9E9E9",
        -100: "#585858",
        -1000: "darkred"
    }
    STATUS = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (70, 'B-'),
        (60, 'C+'),
        (50, 'C'),
        (40, 'C-'),
        (0, 'D'),
        (N_A, 'N/A'),
        (-100, 'COPY'),
        (-1000, 'FAIL'),
    )

    @staticmethod
    def get_code(name):
        for i in StudyRecord_score.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in StudyRecord_score.STATUS:
            if str(code) == str(i[0]):
                return i[1]

    @staticmethod
    def get_color(code):
        try:
            return StudyRecord_score.color_dic[int('code')]
        except:
            return None


class SurveryItem_anwser_type(object):
    score = 'score'
    STATUS = (
        (score, "打分"),
        ('multiple', "多选"),
        ('single', "单选"),
        ('suggestion', "建议")
    )

    @staticmethod
    def get_code(name):
        for i in SurveryItem_anwser_type.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in SurveryItem_anwser_type.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class Compliant_compliant_type(object):
    compliant = 'compliant'
    STATUS = (
        (compliant, u"投诉"),
        ('suggestion', u"建议")
    )

    @staticmethod
    def get_code(name):
        for i in Compliant_compliant_type.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in Compliant_compliant_type.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class Compliant_Status(object):
    unread = 'unread'
    STATUS = (
        (unread, u"未处理"),
        ('sovled', u'已处理'),
        ('pending', u'目前无法解决'),
    )

    @staticmethod
    def get_code(name):
        for i in Compliant_Status.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in Compliant_Status.STATUS:
            if str(code) == str(i[0]):
                return i[1]


def main():
    pass


if __name__ == '__main__':
    main()
