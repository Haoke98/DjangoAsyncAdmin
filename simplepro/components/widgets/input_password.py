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


class PasswordInputWidget(forms.CharField, Input):
    template_name = "admin/components/input_password.html"

    def __init__(self,
                 max_length=48, min_length=6, placeholder=None, clearable=True,
                 show_password=False,
                 show_word_limit=False,
                 disabled=False, readonly=False,
                 size=None,
                 prefix_icon=None, suffix_icon=None, rows=None, autocomplete=None,  # 这几个参数是几乎没有用到，也用不到
                 resize=None, autofocus=False,
                 encrypt: str = "",
                 pattern: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-$%&@+!",
                 style=None,
                 *args, **kwargs):
        super(PasswordInputWidget, self).__init__(*args)
        self.items = {
            'type': 'password',
            'placeholder': placeholder,
            ':clearable': clearable,
            ':show-password': show_password,
            'disabled': disabled,
            'size': size,
            'prefix-icon': prefix_icon,
            'suffix-icon': suffix_icon,
            'rows': rows,
            'autocomplete': autocomplete,
            ':readonly': readonly,
            ':resize': resize,
            ':autofocus': autofocus,
            ':show-word-limit': show_word_limit,
        }
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
        self.encrypt = encrypt
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

    def build_app_data(self):
        pass

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        raw_name = name
        name = trim_name(name)
        ctx = {
            'name': name,
            'raw_name': raw_name,
            'attrs': self.build_attrs(),
            'app_data': {
                'value': conditional_escape(force_text(value)),
                'lenMin': self.min_length,
                'lenMax': self.max_length,
                'pwdPattern': self.pattern,
                'encrypt': force_text(self.encrypt)
            },
            'style': self.style
        }
        _str = render_to_string(self.template_name, ctx)
        return mark_safe(_str)
