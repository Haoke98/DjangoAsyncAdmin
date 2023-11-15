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
from ..widgets import JsonEditorWidget


class JsonTextField(models.TextField):
    """ custom model field """

    def __init__(self, *args, **kwargs):
        self.config_name = kwargs.pop("config_name", "default")
        super(JsonTextField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': JsonTextFormField,
            'config_name': self.config_name
        }
        defaults.update(kwargs)
        return super(JsonTextField, self).formfield(**defaults)


class JsonTextFormField(forms.fields.CharField):
    """ custom form field """

    def __init__(self, config_name='default', *args, **kwargs):
        kwargs.update({
            'widget': JsonEditorWidget(config_name=config_name)
        })
        super(JsonTextFormField, self).__init__(*args, **kwargs)
