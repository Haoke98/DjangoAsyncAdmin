# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/17
@Software: PyCharm
@disc:
======================================="""
from django import forms
from django.db import models

from ..widgets import CharInputWidget


class CharFormField(forms.fields.CharField):
    fields = ['input_type', 'max_length', 'min_length'
        , 'placeholder', 'clearable', 'show_password', 'disabled', 'size',
              'prefix_icon', 'suffix_icon', 'rows', 'autocomplete', 'readonly',
              'max_value', 'min_value', 'step', 'resize', 'autofocus', 'show_word_limit', 'slot', 'slot_text', 'style']

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': CharInputWidget(**kwargs)
        })
        for f in self.fields:
            if f in kwargs:
                kwargs.pop(f)
        super(CharFormField, self).__init__(*args, **kwargs)


class CharField(models.CharField):

    def __init__(self, input_type='text', placeholder=None, clearable=True, show_password=False,
                 min_length=None, disabled=False, size=None, prefix_icon=None, suffix_icon=None, rows=None,
                 autocomplete=None,
                 readonly=None, max_value=None, min_value=None, step=None,
                 resize=None, autofocus=False,
                 show_word_limit=False,
                 slot=None, slot_text='', style=None,
                 *args, **kwargs):
        self.items = {
            'input_type': input_type,
            'max_length': kwargs.get('max_length'),
            'min_length': min_length,
            'placeholder': placeholder,
            'clearable': clearable,
            'show_password': show_password,
            'disabled': disabled,
            'size': size,
            'prefix_icon': prefix_icon,
            'suffix_icon': suffix_icon,
            'rows': rows,
            'autocomplete': autocomplete,
            'readonly': readonly,
            'max_value': max_value,
            'min_value': min_value,
            'step': step,
            'resize': resize,
            'autofocus': autofocus,
            'show_word_limit': show_word_limit,
            'slot': slot,
            'slot_text': slot_text,
            'style': style
        }

        super(CharField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CharFormField,
        }

        defaults.update(kwargs)
        defaults.update(self.items)

        r = super(CharField, self).formfield(**defaults)
        return r