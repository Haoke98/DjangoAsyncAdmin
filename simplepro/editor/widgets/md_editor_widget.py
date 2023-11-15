# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/15
@Software: PyCharm
@disc:
======================================="""
from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

try:

    from django.forms.utils import flatatt
except ImportError:

    from django.forms.util import flatatt

MEDITOR_DEFAULT_CONFIG = {
    'width': '90%',
    'height': 500,
    'toolbar': ["undo", "redo", "|",
                "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                "h1", "h2", "h3", "h5", "h6", "|",
                "list-ul", "list-ol", "hr", "|",
                "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                "emoji", "html-entities", "pagebreak", "goto-line", "|",
                "help", "info",
                "||", "preview", "watch", "fullscreen"],
    'upload_image_formats': ["jpg", "JPG", "jpeg", "JPEG", "gif", "GIF", "png",
                             "PNG", "bmp", "BMP", "webp", "WEBP"],
    'image_floder': 'editor',
    'theme': 'default',
    'preview_theme': 'default',
    'editor_theme': 'default',
    'toolbar_autofixed': True,
    'search_replace': True,
    'emoji': True,
    'tex': True,
    'flow_chart': True,
    'sequence': True,
    'language': 'zh'
}


class MDConfig(dict):

    def __init__(self, config_name='default'):
        self.update(MEDITOR_DEFAULT_CONFIG)
        self.set_configs(config_name)

    def set_configs(self, config_name='default'):
        """
        set config item
        :param config_name:
        :return:
        """

        configs = getattr(settings, 'MDEDITOR_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):

                if config_name in configs:
                    config = configs[config_name]

                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('MDEDITOR_CONFIGS["%s"] \
                                        setting must be a dictionary type.' %
                                                   config_name)

                    self.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                                    found in your CKEDITOR_CONFIGS setting." %
                                               config_name)
            else:
                raise ImproperlyConfigured('MDEDITOR_CONFIGS setting must be a\
                                dictionary type.')


class MDEditorWidget(forms.Textarea):
    """
    Widget providing Editor.md for Rich Text Editing.
    see Editor.md docs: https://pandao.github.io/editor.md/examples/index.html
    """

    def __init__(self, config_name='default', *args, **kwargs):
        super(MDEditorWidget, self).__init__(*args, **kwargs)

        self.config = MDConfig(config_name)

    def render(self, name, value, renderer=None, attrs=None):
        """
        renderer: django2.1 新增加的参数，此处不做应用，赋值None做兼容处理
        """
        if value is None:
            value = ''

        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        return mark_safe(render_to_string('admin/editor/mdeditor/markdown.html', {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_text(value)),
            'id': final_attrs['id'],
            'config': self.config,
        }))

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11+
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs
