# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20151213_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrecord',
            name='consultant',
            field=models.ForeignKey(default=1, verbose_name='\u8d1f\u8d23\u8001\u5e08', to=settings.AUTH_USER_MODEL, help_text='\u8c01\u7b7e\u7684\u5355\u5c31\u9009\u8c01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 8, 2, 11, 838401, tzinfo=utc)),
        ),
    ]
