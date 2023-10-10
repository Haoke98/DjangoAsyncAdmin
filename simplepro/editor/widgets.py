from __future__ import absolute_import

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text
from django.utils.functional import Promise
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


class LazyEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


json_encode = LazyEncoder().encode

UEDITOR_DEFAULT_CONFIG = {
    'UEDITOR_HOME_URL': '/static/admin/ueditor/',
    'toolbars': [[
        'fullscreen', 'source', '|', 'undo', 'redo', '|',
        'bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat',
        'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist',
        'insertunorderedlist', 'selectall', 'cleardoc', '|',
        'rowspacingtop', 'rowspacingbottom', 'lineheight', '|',
        'customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
        'directionalityltr', 'directionalityrtl', 'indent', '|',
        'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
        'link', 'unlink', 'anchor', '|', 'imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
        'simpleupload', 'insertimage', 'emotion', 'scrawl', 'insertvideo', 'music', 'attachment', 'map', 'gmap',
        'insertframe', 'insertcode', 'webapp', 'pagebreak', 'template', 'background', '|',
        'horizontal', 'date', 'time', 'spechars', 'snapscreen', 'wordimage', '|',
        'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol',
        'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols', 'charts', '|',
        'print', 'preview', 'searchreplace', 'drafts', 'help'
    ]],
    'autoFloatEnabled': False
}


class UEConfig(dict):

    def __init__(self, config_name='default'):
        self.update(UEDITOR_DEFAULT_CONFIG)
        self.set_configs(config_name)

    def set_configs(self, config_name='default'):
        """
        set config item
        :param config_name:
        :return:
        """

        configs = getattr(settings, 'UEDITOR_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):

                if config_name in configs:
                    config = configs[config_name]

                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('UEDITOR_CONFIGS["%s"] \
                                        setting must be a dictionary type.' %
                                                   config_name)

                    self.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                                    found in your UEDITOR_CONFIGS setting." %
                                               config_name)
            else:
                raise ImproperlyConfigured('UEDITOR_CONFIGS setting must be a\
                                dictionary type.')


class UEditorWidget(forms.Textarea):
    """
    Widget providing CKEditor for Rich Text Editing.
    Supports direct image uploads and embed.
    """

    def __init__(self, *args, **kwargs):
        super(UEditorWidget, self).__init__(*args, **kwargs)
        self.config = UEConfig()

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        return mark_safe(render_to_string('admin/editor/ueditor/widget.html', {
            'value': conditional_escape(force_text(value)),
            'config': json_encode(self.config),
            'name': name,
        }))
