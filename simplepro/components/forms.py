# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django import forms
from simplepro.components.widgets import PasswordInput


class PasswordFormField(forms.CharField):
    pattern: str
    lenMin: int
    lenMax: int
    encryptByMd5: bool

    def __init__(self, widget=PasswordInput, encryptByMd5: bool = True, lenMin: int = 6, lenMax: int = 48,
                 pattern: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-$%&@+!", *args,
                 **kwargs):
        self.pattern = pattern
        self.lenMin = lenMin
        self.lenMax = lenMax
        self.encryptByMd5 = encryptByMd5
        super().__init__(widget=widget, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, PasswordInput):
            attrs['pattern'] = self.pattern
            attrs['lenMin'] = self.lenMin
            attrs['lenMax'] = self.lenMax
            attrs['encryptByMd5'] = self.encryptByMd5
        return attrs
