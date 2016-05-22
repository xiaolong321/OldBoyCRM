# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Username")}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Password")}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                classes = self.fields[f_name].widget.attrs.get('class', '')
                classes += ' has-error'
                self.fields[f_name].widget.attrs['class'] = classes

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            if settings.LDAP_CHECK:
                from backend.commons.ldaptest2 import LDAPTool
                from ..web_models.myauth import UserProfile

                try:
                    if username.startswith('admin'):
                        raise Exception(u'admin 账户不进行验证')
                    if LDAPTool().ldap_get_vaild(uid=username, passwd=password):
                        username_info = LDAPTool().ldap_get_user(uid=username)
                        logger.debug(u'查询到用户信息 %s' % username)
                        try:
                            # 更新本地账户 用户名密码
                            user = UserProfile.objects.get(email=username_info['mail'])
                            user.set_password("%s" % str(password))
                            user.save()
                        except:
                            # 如果没有 则进行创建
                            UserProfile.objects.create_user(
                                email=username_info['mail'],
                                name=username_info['displayName'],
                                password="%s" % str(password),
                            ).save()
                except Exception as e:
                    print e
                    pass
            try:
                if username.startswith('admin'):
                    user_email = username
                    raise Exception(u'')
                if LDAPTool().ldap_get_vaild(uid=username, passwd=password):
                    user_email = LDAPTool().ldap_get_user(uid=username)['mail']
            except Exception as e:
                user_email = username
                print e
            try:
                self.user_cache = authenticate(
                    email=user_email,
                    password=password
                )
            except Exception as e:
                print e.message
                pass
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Username")}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _("Email Address")}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Password")}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Confirm your password")}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' has-error'
                    self.fields[f_name].widget.attrs['class'] = classes

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        # _("Account already exists.")
        raise forms.ValidationError("用户名已经存在,请更换!")

    def clean_password2(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                # _("Passwords don't match.")
                raise forms.ValidationError("两次输入的密码不一致!")
        return self.cleaned_data['password2']

    def clean(self):
        return self.cleaned_data
