# coding=utf-8
#系统层敞亮
__author__ = 'lyhapple'

DEFAULT_DASHBOARD_TITLE = u'首页'

MALE = 'male'
FEMALE = 'female'

SEX = (
    (MALE, u'男'),
    (FEMALE, u'女'),
)

TRUE_FALSE = (
    (True, u'是'),
    (False, u'否')
)

DICT_NULL_BLANK_TRUE = {
    # 默认demols 状态
    'null': True,
    'blank': True
}


class ReadStatus(object):
    """
    读取状态
    """
    UNREAD = 0
    READ = 1
    DELETED = 99
    STATUS = (
        (UNREAD, u'未读'),
        (READ, u'已读'),
        (DELETED, u'删除'),
    )


class MailStatus(object):
    """
    邮件系统状态
    """
    UNREAD = 0
    READ = 1
    DRAFT = 2
    TRASH = 3
    DELETED = 99
    STATUS = (
        (UNREAD, u'未读'),
        (READ, u'已读'),
        (DRAFT, u'草稿'),
        (TRASH, u'回收站'),
        (DELETED, u'删除'),
    )


class UsableStatus(object):
    """
    默认状态
    """
    UNUSABLE = 0
    USABLE = 1
    DELETED = 99
    STATUS = (
        (UNUSABLE, u'禁用'),
        (USABLE, u'启用'),
        (DELETED, u'删除'),
    )


class RequestType(object):
    """
    默认状态
    """
    GET = 0
    POST = 1
    STATUS = (
        (GET, u'get'),
        (POST, u'post'),
    )

    @staticmethod
    def get_code(name):
        for i in RequestType.STATUS:
            if str(name) == str(i[1]):
                return i[0]

    @staticmethod
    def get_name(code):
        for i in RequestType.STATUS:
            if str(code) == str(i[0]):
                return i[1]


class TaskStatus(object):
    """
    任务状态
    """
    NORMAL = 0
    EXCEPT = 1
    ther = 3
    FINISHED = 2
    DELETED = 99
    TASK_STATUS = (
        (ther, u'等待客户端部署'),
        (NORMAL, u'正常(进行中)'),
        (EXCEPT, u'异常'),
        (FINISHED, u'完成'),
        (DELETED, u'删除')
    )


class Position(object):
    """
    职工状态
    """
    STAFF = 0
    MANAGE = 1
    VICE_PRESIDENT = 2
    PRESIDENT = 3

    POSITIONS = (
        (STAFF, u'职工'),
        (MANAGE, u'经理'),
        (VICE_PRESIDENT, u'副总裁'),
        (PRESIDENT, u'总裁'),
    )

class Asset_Status(object):
    """
    设备状态
    """
    UNUSABLE = 0
    USABLE = 1
    MAINTAIN = 2
    DELETED = 99
    STATUS = (
        (UNUSABLE, u'尚未启用'),
        (USABLE, u'使用中'),
        (MAINTAIN, u'维护中'),
        (DELETED, u'废弃'),
    )

class OnlineMode(object):
    """
    项目类型
    """
    TOMCAT = 0
    NGINX = 1
    DUBBO = 2
    STATUS = (
        (TOMCAT,U'TOMCAT'),
        (NGINX,u'nginx'),
        (DUBBO,u'dubbo'),
    )

class Online_Batch(object):
    ONE = 1
    TOW = 2
    THER = 3
    STATUS = (
        (ONE,u'第一批次'),
        (TOW,u'第二批次'),
        (THER,u'第三批次'),
    )