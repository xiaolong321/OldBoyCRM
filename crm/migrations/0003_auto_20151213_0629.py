# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20151213_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(verbose_name='\u8ddf\u8fdb\u5185\u5bb9...')),
                ('status', models.IntegerField(help_text='\u9009\u62e9\u5ba2\u6237\u6b64\u65f6\u7684\u72b6\u6001', verbose_name='\u72b6\u6001', choices=[(1, '\u8fd1\u671f\u65e0\u62a5\u540d\u8ba1\u5212'), (2, '2\u4e2a\u6708\u5185\u62a5\u540d'), (3, '1\u4e2a\u6708\u5185\u62a5\u540d'), (4, '2\u5468\u5185\u62a5\u540d'), (5, '1\u5468\u5185\u62a5\u540d'), (6, '2\u5929\u5185\u62a5\u540d'), (7, '\u5df2\u62a5\u540d'), (8, '\u5df2\u4ea4\u5168\u6b3e')])),
                ('date', models.DateField(auto_now_add=True, verbose_name='\u8ddf\u8fdb\u65e5\u671f')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qq', models.CharField(help_text='QQ\u53f7\u5fc5\u987b\u552f\u4e00', unique=True, max_length=64)),
                ('qq_name', models.CharField(max_length=64, null=True, verbose_name='QQ\u540d\u79f0', blank=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name='\u59d3\u540d', blank=True)),
                ('phone', models.IntegerField(null=True, verbose_name='\u624b\u673a\u53f7', blank=True)),
                ('source', models.CharField(default=b'qq', max_length=64, verbose_name='\u5ba2\u6237\u6765\u6e90', choices=[(b'qq', 'qq\u7fa4'), (b'referral', '\u5185\u90e8\u8f6c\u4ecb\u7ecd'), (b'51cto', '51cto'), (b'others', '\u5176\u5b83')])),
                ('course', models.CharField(max_length=64, verbose_name='\u54a8\u8be2\u8bfe\u7a0b', choices=[(b'LinuxL1', 'Linux\u4e2d\u9ad8\u7ea7'), (b'LinuxL2', 'Linux\u67b6\u6784\u5e08'), (b'PythonDevOps', 'Python\u81ea\u52a8\u5316\u5f00\u53d1')])),
                ('class_type', models.CharField(max_length=64, verbose_name='\u73ed\u7ea7\u7c7b\u578b', choices=[(b'online', '\u7f51\u7edc\u73ed'), (b'offline_weekend', '\u9762\u6388\u73ed(\u5468\u672b)'), (b'offline_fulltime', '\u9762\u6388\u73ed(\u8131\u4ea7)')])),
                ('customer_note', models.TextField(help_text='\u5ba2\u6237\u54a8\u8be2\u7684\u5927\u6982\u60c5\u51b5,\u5ba2\u6237\u4e2a\u4eba\u4fe1\u606f\u5907\u6ce8\u7b49...', verbose_name='\u54a8\u8be2\u5185\u5bb9\u5907\u6ce8')),
                ('status', models.CharField(default='unregistered', help_text='\u9009\u62e9\u5ba2\u6237\u6b64\u65f6\u7684\u72b6\u6001', max_length=64, verbose_name='\u72b6\u6001', choices=[(b'signed', '\u5df2\u62a5\u540d'), (b'unregistered', '\u672a\u62a5\u540d'), (b'paid_in_full', '\u5b66\u8d39\u5df2\u4ea4\u9f50')])),
                ('paid_fee', models.IntegerField(default=0, null=True, verbose_name='\u5df2\u4ea4\u8d39\u7528', blank=True)),
                ('date', models.DateField(auto_now_add=True, verbose_name='\u54a8\u8be2\u65e5\u671f')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='valid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 12, 6, 29, 40, 362165, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='customer',
            name='course_consultant',
            field=models.ForeignKey(verbose_name='\u8bfe\u7a0b\u987e\u95ee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consultrecord',
            name='consultant',
            field=models.ForeignKey(verbose_name='\u8ddf\u8e2a\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consultrecord',
            name='customer',
            field=models.ForeignKey(verbose_name='\u6240\u54a8\u8be2\u5ba2\u6237', to='crm.Customer'),
        ),
    ]
