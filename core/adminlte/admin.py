#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
from django.contrib import admin
logger = logging.getLogger(__name__)

from .web_models import models
######################################################################
# 自定义 user 方法
from .web_models.myauth_admin import UserProfileAdmin
from .web_models.myauth import Permission_Api_Action, Permission_Api_objects, Groups, Group
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(Permission_Api_Action)
admin.site.register(Permission_Api_objects)
#admin.site.unregister(Group)
@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions', 'group_api_permissions')

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super(GroupAdmin, self).formfield_for_manytomany(
            db_field, request=request, **kwargs)

######################################################################
admin.site.register(models.SystemConfig, models.SystemConfigAdmin)
admin.site.register(models.Menu, models.MenuAdmin)
admin.site.register(models.Resource, models.ResourceAdmin)
admin.site.register(models.Permission, models.PermissionAdmin)

def main():
    pass


if __name__ == '__main__':
    main()
