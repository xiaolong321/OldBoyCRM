# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20151213_0639'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.CharField(max_length=64, verbose_name='\u8bfe\u7a0b\u540d', choices=[(b'LinuxL1', 'Linux\u4e2d\u9ad8\u7ea7'), (b'LinuxL2', 'Linux\u67b6\u6784\u5e08'), (b'PythonDevOps', 'Python\u81ea\u52a8\u5316\u5f00\u53d1')])),
                ('class_type', models.CharField(max_length=64, verbose_name='\u73ed\u7ea7\u7c7b\u578b', choices=[(b'online', '\u7f51\u7edc\u73ed'), (b'offline_weekend', '\u9762\u6388\u73ed(\u5468\u672b)'), (b'offline_fulltime', '\u9762\u6388\u73ed(\u8131\u4ea7)')])),
                ('pay_type', models.CharField(default=b'deposit', max_length=64, verbose_name='\u8d39\u7528\u7c7b\u578b', choices=[(b'deposit', '\u8ba2\u91d1/\u62a5\u540d\u8d39'), (b'tution', '\u5b66\u8d39'), (b'refund', '\u9000\u6b3e')])),
                ('paid_fee', models.IntegerField(default=0, verbose_name='\u8d39\u7528\u6570\u989d')),
                ('note', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u4ea4\u6b3e\u65e5\u671f')),
            ],
            options={
                'verbose_name': '\u4ea4\u6b3e\u7eaa\u5f55',
                'verbose_name_plural': '\u4ea4\u6b3e\u7eaa\u5f55',
            },
        ),
        migrations.RemoveField(
            model_name='customer',
            name='paid_fee',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 7, 6, 2, 994052, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='customer',
            field=models.ForeignKey(verbose_name='\u5ba2\u6237', to='crm.Customer'),
        ),
    ]
