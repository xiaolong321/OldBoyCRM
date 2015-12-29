# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20151213_0802'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.CharField(max_length=64, verbose_name='\u8bfe\u7a0b\u540d\u79f0', choices=[(b'LinuxL1', 'Linux\u4e2d\u9ad8\u7ea7'), (b'LinuxL2', 'Linux\u67b6\u6784\u5e08'), (b'PythonDevOps', 'Python\u81ea\u52a8\u5316\u5f00\u53d1')])),
                ('semester', models.IntegerField(verbose_name='\u5b66\u671f')),
                ('start_date', models.DateField(verbose_name='\u5f00\u73ed\u65e5\u671f')),
            ],
            options={
                'verbose_name': '\u73ed\u7ea7\u5217\u8868',
                'verbose_name_plural': '\u73ed\u7ea7\u5217\u8868',
            },
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 8, 39, 58, 645375, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u8bb2\u5e08'),
        ),
        migrations.AddField(
            model_name='customer',
            name='class_list',
            field=models.ManyToManyField(to='crm.ClassList', blank=True),
        ),
    ]
