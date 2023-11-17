# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django import forms
from django.db import models

from simplepro.components.widgets import PasswordInputWidget


class PasswordFormField(forms.CharField):
    fields = ['input_type', 'max_length', 'min_length'
        , 'placeholder', 'clearable', 'show_password', 'disabled', 'size',
              'prefix_icon', 'suffix_icon', 'rows', 'autocomplete', 'readonly',
              'max_value', 'min_value', 'step', 'resize', 'autofocus', 'show_word_limit', 'slot', 'slot_text', 'style',
              'pattern', 'encrypt']

    def __init__(self,
                 encrypt: str = None,
                 pattern: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-$%&@+!",
                 *args, **kwargs):
        kwargs.update({
            'widget': PasswordInputWidget(pattern=pattern, encrypt=encrypt, **kwargs)
        })
        for f in self.fields:
            if f in kwargs:
                kwargs.pop(f)
        super(PasswordFormField, self).__init__(*args, **kwargs)


class PasswordInputField(models.CharField):
    """ custom model field """

    def __init__(self,
                 min_length=6,
                 placeholder=None, clearable=True, show_password=True,
                 show_word_limit=False, disabled=False, readonly=False,
                 size=None,
                 autofocus=False,
                 style=None,
                 encrypt: str = None,
                 pattern: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-$%&@+!",
                 *args, **kwargs):

        self.items = {
            'max_length': kwargs.get('max_length'),
            'min_length': min_length,
            'placeholder': placeholder,
            'clearable': clearable,
            'show_password': show_password,
            'disabled': disabled,
            'readonly': readonly,
            'show_word_limit': show_word_limit,
            'size': size,
            'autofocus': autofocus,
            'encrypt': encrypt,
            'pattern': pattern,
            'style': style
        }
        super(PasswordInputField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': PasswordFormField,
        }
        defaults.update(self.items)
        r = super(PasswordInputField, self).formfield(**defaults)
        return r
