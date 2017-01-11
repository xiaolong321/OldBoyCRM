# !/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from OldboyCRM import settings
import zipfile
import os


@shared_task
def uploadhomework(class_id, day_num, upload_path):
    customer_file_path = "%s/%s/%s" % (settings.HOMEWORK_DATA_DIR, class_id, day_num,)
    filename = '%s.zip' % upload_path.split('/')[-2]
    zipfile_path = "%s/%s" % (settings.HOMEWORK_DATA_DIR, class_id)
    zipfile_obj = zipfile.ZipFile("%s/%s" % (zipfile_path, filename), 'a', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(customer_file_path):
        print(dirpath, dirnames, filenames)
        for file in filenames:
            if file.endswith('.zip'):
                f = zipfile.ZipFile(os.path.join(dirpath, file), 'r')
                for file_obj in f.namelist():
                    unzipfile = f.extract(file_obj, os.path.join(customer_file_path, 'all',
                                                                 file.split('.zip')[0]))
                    zipfile_obj.write(unzipfile, os.path.join(file.split('.zip')[0], file_obj))
    zipfile_obj.close()

