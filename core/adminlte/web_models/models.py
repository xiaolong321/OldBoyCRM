#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'
import logging
from .constants import UsableStatus, DICT_NULL_BLANK_TRUE
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.contrib.auth.models import Group
from django.db import models
from django.contrib import admin

logger = logging.getLogger(__name__)
from myauth import UserProfile


class BaseModel(models.Model):
    """
    基础表信息.用于继承
    """
    creator = models.ForeignKey(
        UserProfile,
        verbose_name=u"数据更新人",
        **DICT_NULL_BLANK_TRUE
    )
    created_at = models.DateTimeField(
        verbose_name=u"数据创建时间",
        default=timezone.now
    )
    updated_at = models.DateTimeField(
        verbose_name=u"数据更新时间",
        default=timezone.now
    )
    deleted_at = models.DateTimeField(
        verbose_name=u"数据删除时间",
        **DICT_NULL_BLANK_TRUE
    )

    class Meta:
        abstract = True


class SystemConfig(MPTTModel, BaseModel, UsableStatus):
    name = models.CharField(
        u"键", max_length=255, unique=True
    )
    value = models.CharField(
        u"值", max_length=255
    )
    title = models.CharField(
        u"描述", max_length=255
    )
    parent = TreeForeignKey(
        'self', verbose_name=u'父配置项',
        related_name='children', db_index=True,
        **DICT_NULL_BLANK_TRUE
    )
    status = models.PositiveSmallIntegerField(
        u'状态', choices=UsableStatus.STATUS,
        default=UsableStatus.USABLE, db_index=True
    )

    def __unicode__(self):
        return u"%s" % self.value

    class Meta:
        verbose_name_plural = verbose_name = u"基础-参数配置"

    class MPTTMeta:
        order_insertion_by = ['name']


class Menu(MPTTModel, BaseModel, UsableStatus):
    name = models.CharField(
        u'菜单名称', max_length=50, unique=True
    )
    icon = models.CharField(
        u'菜单图标', max_length=50, default='fa-circle-o',
        help_text=u'参考:http://fontawesome.io'
    )
    parent = TreeForeignKey(
        'self', verbose_name=u'上级菜单',
        related_name='children',
        db_index=True,
        **DICT_NULL_BLANK_TRUE
    )
    app_name = models.CharField(
        u'所属应用', max_length=200,
        **DICT_NULL_BLANK_TRUE
    )
    model_name = models.CharField(
        u'所属模型', max_length=200,
        **DICT_NULL_BLANK_TRUE
    )
    url = models.CharField(
        u'全路径', max_length=200,
        help_text=u'选填', **DICT_NULL_BLANK_TRUE
    )
    order = models.PositiveSmallIntegerField(
        u'排序', default=0
    )
    status = models.PositiveSmallIntegerField(
        u'状态', choices=UsableStatus.STATUS,
        default=UsableStatus.USABLE, db_index=True
    )

    def __unicode__(self):
        return u'%s(%s)' % (self.name, self.order)

    class Meta:
        verbose_name = u'基础-菜单'
        verbose_name_plural = u"基础-菜单"
        ordering = ('order',)

    class MPTTMeta:
        order_insertion_by = ['order']


class Resource(BaseModel, UsableStatus):
    name = models.CharField(
        u'资源名称', max_length=50
    )
    app_name = models.CharField(
        u'所属应用', max_length=200,
        **DICT_NULL_BLANK_TRUE
    )
    model_name = models.CharField(
        u'所属模型', max_length=200,
        **DICT_NULL_BLANK_TRUE
    )
    url = models.CharField(
        u'资源地址', max_length=500,
        help_text=u'API地址',
        **DICT_NULL_BLANK_TRUE
    )
    note = models.CharField(
        u'备注', max_length=500,
        **DICT_NULL_BLANK_TRUE
    )
    status = models.PositiveSmallIntegerField(
        u'状态', choices=UsableStatus.STATUS,
        default=UsableStatus.USABLE, db_index=True
    )

    def __unicode__(self):
        return u'%s(%s)' % (self.name, self.note)

    class Meta:
        verbose_name_plural = verbose_name = u'基础-资源'


class Permission(BaseModel, UsableStatus):
    group = models.ForeignKey(
        Group, verbose_name=u'角色',
        related_name='group_permission'
    )
    menus = models.ManyToManyField(
        Menu, verbose_name=u'菜单',
        blank=True
    )
    resources = models.ManyToManyField(
        Resource, verbose_name=u'资源',
        blank=True
    )
    status = models.PositiveSmallIntegerField(
        u'状态', choices=UsableStatus.STATUS,
        default=UsableStatus.USABLE, db_index=True
    )

    def __unicode__(self):
        return self.group.name

    class Meta:
        verbose_name_plural = verbose_name = u'基础-首要配置-权限'


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'status')
    list_filter = ('status',)
    fieldsets = (
        (u'角色', {'fields': ('group',)}),
        # ('API TOKEN info', {'fields': ('token',)}),
        (u'资源', {'fields': ('menus', 'resources')}),
        (u'状态', {'fields': ('status',)}),
    )

    search_fields = ('group',)
    ordering = ('group',)


class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'status', 'parent', 'title')
    list_filter = ('status',)
    fieldsets = (
        (u'父选项', {'fields': ('parent',)}),
        (u'内容', {'fields': ('name', 'value', 'title')}),
        (u'状态', {'fields': ('status',)}),
        (u'创建人', {'fields': ('creator',)}),
        (u'操作记录', {'fields': ('created_at', 'updated_at', 'deleted_at')})
    )
    search_fields = ('name',)
    ordering = ('name',)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'app_name', 'model_name', 'url', 'status')
    list_filter = ('status',)
    fieldsets = (
        (u'父选项', {'fields': ('parent',)}),
        (u'内容', {'fields': ('name', 'icon', 'app_name', 'model_name', 'url', 'order')}),
        (u'状态', {'fields': ('status',)}),
        (u'创建人', {'fields': ('creator',)}),
        (u'操作记录', {'fields': ('created_at', 'updated_at', 'deleted_at')})
    )
    search_fields = ('name',)
    ordering = ('name',)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'app_name', 'model_name', 'url', 'status')
    list_filter = ('status',)
    fieldsets = (
        (u'内容', {'fields': ('name', 'app_name', 'model_name', 'url', 'note')}),
        (u'状态', {'fields': ('status',)}),
        (u'创建人', {'fields': ('creator',)}),
        (u'操作记录', {'fields': ('created_at', 'updated_at', 'deleted_at')})
    )
    search_fields = ('name',)
    ordering = ('name',)


def main():
    pass


if __name__ == '__main__':
    main()
