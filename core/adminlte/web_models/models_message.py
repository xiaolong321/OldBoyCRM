#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
from .constants import UsableStatus, DICT_NULL_BLANK_TRUE, MailStatus
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db import models
from django.contrib import admin

logger = logging.getLogger(__name__)
from .models import BaseModel
from .myauth import UserProfile


class MyMessage(BaseModel):
    """
    基础表信息.用于继承
    """
    receive_user = models.ForeignKey(
        UserProfile,
        verbose_name=u"接收人",
        related_name='receive_user',
    )
    Message = models.TextField(
        verbose_name=u'json接口',
        help_text=u'短信的json 接口 用于直接给前端.勿动!!!!',
        **DICT_NULL_BLANK_TRUE
    )
    Status = models.PositiveSmallIntegerField(
        u'状态',
        choices=MailStatus.STATUS,
        default=MailStatus.UNREAD,
        db_index=True
    )

    def __unicode__(self):
        return u"%s" % self.receive_user

    class Meta:
        verbose_name_plural = verbose_name = u"基础-消息中心"



class MyMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'receive_user', 'Status')
    fieldsets = (
        (u'接收人', {'fields': ('receive_user',)}),
        (u'内容', {'fields': ('Message',)}),
        (u'发送人', {'fields': ('creator',)}),
        (u'状态', {'fields': ('Status',)}),
        (u'操作记录', {'fields': ('created_at', 'updated_at', 'deleted_at')})
    )


def main():
    pass


if __name__ == '__main__':
    main()
