#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime
from datetime import date
import logging
logger = logging.getLogger(__name__)

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)