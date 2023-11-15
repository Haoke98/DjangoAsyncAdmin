# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django import forms
from django.template.loader import render_to_string
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .input import Input, trim_name

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text


class NumberInputWidget(forms.IntegerField, Input):
    class Media:
        pass

    def __init__(self, max_value, min_value, *args, **kwargs):
        super(NumberInputWidget, self).__init__(*args, **kwargs)
        self.max_value = max_value
        self.min_value = min_value

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/components/input_number.html', {
            'value': conditional_escape(force_text(value)),
            'name': trim_name(name),
            'raw_name': name,
            'max_value': self.max_value,
            'min_value': self.min_value
        }))
