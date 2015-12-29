# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20151213_0629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultrecord',
            options={'verbose_name': '\u5ba2\u6237\u8ddf\u8fdb\u8bb0\u5f55', 'verbose_name_plural': '\u5ba2\u6237\u8ddf\u8fdb\u8bb0\u5f55'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '\u5ba2\u6237\u54a8\u8be2\u4fe1\u606f\u8868', 'verbose_name_plural': '\u5ba2\u6237\u54a8\u8be2\u4fe1\u606f\u8868'},
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='course_consultant',
            new_name='consultant',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 6, 39, 30, 826325, tzinfo=utc)),
        ),
    ]
