#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from crm.models import MessageTemplate

class message:

    def __init__(self, subject, toaddrs):
        self.subject = subject
        self.toaddrs = toaddrs

    def getcontent(self, username=None, classname=None, account=None, password=None):
        if self.subject == 'createaccount':
            content_template = MessageTemplate.objects.filter(subject=self.subject).first().content
            content = content_template.format(username = username, classname = classname, account = account, password = password)
            self.content = content
            self.subject = '创建新用户'


    def sendmessage(self):
        from_email = settings.DEFAULT_FROM_EMAIL
        # subject 主题 content 内容 to_addr 是一个列表，发送给哪些人
        msg = EmailMultiAlternatives(self.subject, self.content, from_email, self.toaddrs)
        msg.content_subtype = "html"
        # 添加附件（可选）
        # msg.attach_file('./twz.pdf')
        # 发送
        msg.send()