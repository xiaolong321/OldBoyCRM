#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

def validate_ipv4(value):
    ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    if not ipv4_re.match(value):
        raise ValidationError('IP格式错误')


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')