# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='token',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 4, 1, 26, 365317, tzinfo=utc)),
        ),
    ]
