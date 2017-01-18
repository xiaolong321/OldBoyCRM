# !/usr/bin/env python
# -*- coding:utf-8 -*-


from django import template
from django.utils.safestring import mark_safe
import os

register = template.Library()


@register.simple_tag
def homework_download_button(homework_path):
    file_path = homework_path
    if os.path.exists(file_path):
        result = "<a href=/file_download/?file_path={}>作业下载</a>".format(file_path)
    else:
        result = "未交作业"
    return mark_safe(result)
