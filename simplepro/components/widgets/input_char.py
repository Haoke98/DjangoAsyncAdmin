# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/17
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


class CharInputWidget(forms.CharField, Input):
    """
    文本输入框
    """

    class Media:
        pass

    def __init__(self, input_type='text', placeholder=None, clearable=True, show_password=False,
                 min_length=None, disabled=False, size=None, prefix_icon=None, suffix_icon=None, rows=None,
                 autocomplete=None,
                 readonly=None, max_value=None, min_value=None, step=None, resize=None, autofocus=False,
                 show_word_limit=False, slot=None, slot_text='', style=None, *args, **kwargs):
        super(CharInputWidget, self).__init__(*args)
        self.items = {
            'type': input_type,
            'placeholder': placeholder,
            ':clearable': clearable,
            ':show-password': show_password,
            'disabled': disabled,
            'size': size,
            'prefix-icon': prefix_icon,
            'suffix-icon': suffix_icon,
            'rows': rows,
            'autocomplete': autocomplete,
            'readonly': readonly,
            'maxlength': kwargs.get('max_length'),
            'minlength': min_length,
            'max': max_value,
            'min': min_value,
            'step': step,
            'resize': resize,
            'autofocus': autofocus,
            ':show-word-limit': show_word_limit,

        }
        self.slot = slot
        self.slot_text = slot_text
        self.style = style

    def build_attrs(self):
        attrs = ""
        for f in self.items:
            val = self.items.get(f)
            if f == 'disabled' and not val:
                continue
            if val is not None:
                if isinstance(val, bool):
                    val = str(val).lower()
                attrs += '\t{}=\"{}\"'.format(f, val)

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        raw_name = name
        name = trim_name(name)

        return mark_safe(render_to_string('admin/components/char.html', {
            'value': conditional_escape(force_text(value)),
            'name': name,
            'raw_name': raw_name,
            'attrs': self.build_attrs(),
            'slot': self.slot,
            'slot_text': self.slot_text,
            'style': self.style
        }))
