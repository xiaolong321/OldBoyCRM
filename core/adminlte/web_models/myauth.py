# _*_coding:utf-8_*_
__author__ = 'jieli'
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
)
from django.utils import timezone
from .constants import UsableStatus, DICT_NULL_BLANK_TRUE, RequestType
import django


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            # token=token,
            # department=department,
            # tel=tel,
            # memo=memo,

        )

        user.set_password(password)
        # user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                name=name,
                                # token=token,
                                # department=department,
                                # tel=tel,
                                # memo=memo,
                                )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Permission_Api_objects(models.Model, UsableStatus):
    action_name = models.CharField(
        u'调用 方法名称',
        max_length=255,
        help_text=u'在传入 api 中 action_name 是必填项目',
        unique=True
    )
    memo = models.TextField(
        u'备注',
        help_text=u'方法备注',
        **DICT_NULL_BLANK_TRUE
    )
    status = models.PositiveSmallIntegerField(
        u'状态', choices=UsableStatus.STATUS,
        default=UsableStatus.USABLE, db_index=True
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

    def __unicode__(self):
        return '%s' % self.action_name

    class Meta:
        verbose_name_plural = verbose_name = u'基础-api层-基础配置'


class Permission_Api_Action(models.Model, UsableStatus):
    action_objects = models.ForeignKey(
        u'Permission_Api_objects',
        verbose_name=u'action_name',
        related_name='Api_objects',
        help_text=u'在传入 api 中 action_name 的 objects 方法 是必填项目',
    )
    action = models.CharField(
        u'方法',
        max_length=255,
        help_text=u'在传入 api 中 action 是必填项目',
    )
    Type = models.PositiveSmallIntegerField(
        u'请求类型',
        choices=RequestType.STATUS,
        **DICT_NULL_BLANK_TRUE
    )
    memo = models.TextField(
        u'备注',
        help_text=u'方法备注',
        **DICT_NULL_BLANK_TRUE
    )
    status = models.PositiveSmallIntegerField(
        u'状态', choices=UsableStatus.STATUS,
        default=UsableStatus.USABLE,
        db_index=True
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

    def __unicode__(self):
        return "应用:%s,调用方法:%s, 类型:%s" % (
            self.action_objects.action_name,
            self.action,
            RequestType.get_name(code=self.Type)
        )

    class Meta:
        verbose_name_plural = verbose_name = u'基础-api层-配置'

class Groups(Group):
    group_api_permissions = models.ManyToManyField(
        Permission_Api_Action,
        verbose_name=u'权限管理',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="group_set_api",
        related_query_name="group_api",
    )
PermissionsMixin.groups = models.ManyToManyField(
    Groups,
    verbose_name=_('groups'),
    blank=True,
    help_text=_(
        'The groups this user belongs to. A user will get all permissions '
        'granted to each of their groups.'
    ),
    related_name="groups_set",
    related_query_name="groups",
)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(u'活跃', default=True)
    is_admin = models.BooleanField(u'超级管理员', default=False)
    name = models.CharField(u'名字', max_length=32)
    department = models.CharField(u'部门', max_length=32, default=None, blank=True, null=True)
    # business_unit = models.CharField(max_length=1)
    tel = models.CharField(u'座机', max_length=32, default=None, blank=True, null=True)
    mobile = models.CharField(u'手机', max_length=32, default=None, blank=True, null=True)

    memo = models.TextField(u'备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, auto_now_add=True)
    # valid_begin = models.DateTimeField(blank=True, auto_now=True)
    valid_begin_time = models.DateTimeField(default=django.utils.timezone.now)
    valid_end_time = models.DateTimeField(default=django.utils.timezone.now)
    avatar = models.ImageField(
        u'头像',
        upload_to='adminlte/user_avatar',
        default=None,
        **DICT_NULL_BLANK_TRUE
    )
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']
    user_api_permissions = models.ManyToManyField(
        Permission_Api_Action,
        verbose_name=u'权限管理',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set_api",
        related_query_name="user_api",
    )

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    '''@property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    '''

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u"用户信息"

    def __unicode__(self):
        return self.name

    objects = UserManager()
