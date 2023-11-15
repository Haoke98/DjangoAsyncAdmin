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

from simplepro.components.widgets import RadioInput


class RadioFormField(forms.fields.IntegerField):
    """ custom form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': RadioInput()
        })
        super(RadioFormField, self).__init__(*args, **kwargs)


class RadioField(models.IntegerField):
    """ custom model field """

    def __init__(self, *args, **kwargs):
        super(RadioField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': RadioFormField,
        }
        defaults.update(kwargs)
        r = super(RadioField, self).formfield(**defaults)

        r.widget = RadioInput(choices=self.choices)
        return r
