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
from ..widgets import NumberInputWidget


class InputNumberFormField(forms.fields.IntegerField):
    """ custom form field """

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': NumberInputWidget(max_value=kwargs.get('max_value'), min_value=kwargs.get('min_value'))
        })
        super(InputNumberFormField, self).__init__(*args, **kwargs)


class InputNumberField(models.IntegerField):
    """
     InputNumberField
     document: https://simpleui.72wo.com/docs/simplepro/components.html
    """
    max_value = None
    min_value = None

    def __init__(self, *args, **kwargs):
        if 'max_value' in kwargs:
            max_value = kwargs.pop('max_value')
            self.max_value = max_value
        if 'min_value' in kwargs:
            min_value = kwargs.pop('min_value')
            self.min_value = min_value
        super(InputNumberField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': InputNumberFormField,
            'min_value': self.min_value,
            'max_value': self.max_value
        }
        defaults.update(kwargs)
        r = super(InputNumberField, self).formfield(**defaults)

        r.widget = NumberInputWidget(max_value=self.max_value, min_value=self.min_value)
        return r
