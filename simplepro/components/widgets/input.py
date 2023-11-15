# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django.utils import formats


def trim_name(name):
    return name.replace('-', '_')


class Input:
    needs_multipart_form = False
    is_hidden = False
    attrs = {}
    is_required = False

    def get_context(self, name, value, attrs):
        context = {}
        context['widget'] = {
            'name': name,
            'is_hidden': self.is_hidden,
            'required': self.is_required,
            'value': self.format_value(value),
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name,
        }
        return context

    def format_value(self, value):
        """
        返回在模板中呈现时应该出现的值。
        """
        if value == '' or value is None:
            return None
        if self.is_localized:
            return formats.localize_input(value)
        return str(value)

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of item and this widget's name, return the value
        of this widget or None if it's not provided.
        """
        return data.get(name)

    def id_for_label(self, id_):
        """
        给定字段的ID，返回此小部件的HTML ID属性，以供<label>使用。
        如果没有可用的ID，则返回None。
        这个钩子是必需的，因为一些小部件有多个HTML元素，因此有多个id。
        在这种情况下，这个方法应该返回一个ID值，该值对应于小部件标记中的第一个ID。
        """
        return id_

    def use_required_attribute(self, initial):
        return not self.is_hidden

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build an attribute dictionary."""
        return {**base_attrs, **(extra_attrs or {})}

    def value_omitted_from_data(self, data, files, name):
        return name not in data

    def get_bind_attr(self, attrs=None):
        """
        获取该控件需要绑定的变量参数
        :return:
        """
        if not attrs:
            self.bind_attr = {}
            return
        for key, value in attrs.items():
            if key[0] == ":":
                if isinstance(value, str):
                    self.bind_attr[value] = ''
                elif isinstance(value, dict):
                    for a, b in value.items():
                        self.bind_attr[a] = b
                else:
                    continue
