# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20151213_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 7, 54, 46, 421528, tzinfo=utc)),
        ),
    ]
