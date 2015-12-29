# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20151213_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='referral_from',
            field=models.ForeignKey(related_name='internal_referral', blank=True, to='crm.Customer', help_text='\u82e5\u6b64\u5ba2\u6237\u662f\u8f6c\u4ecb\u7ecd\u81ea\u5185\u90e8\u5b66\u5458,\u8bf7\u5728\u6b64\u5904\u9009\u62e9\u5185\u90e8\u5b66\u5458\u59d3\u540d', null=True, verbose_name='\u8f6c\u4ecb\u7ecd\u81ea\u5b66\u5458'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 7, 16, 10, 318594, tzinfo=utc)),
        ),
    ]
