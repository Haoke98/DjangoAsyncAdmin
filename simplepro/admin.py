from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

LIST_DISPLAY = ['id', 'updatedAt', 'createdAt']


class FieldOptions:
    IP_ADDRESS = {
        'min_width': "140px",
        'align': 'left'
    }
    MAC_ADDRESS = {
        'min_width': "180px",
        'align': 'left'
    }
    UUID = {
        'fixed': 'left',
        'min_width': '80px',
        'align': 'center',
        "resizeable": True,
        "show_overflow_tooltip": True
    }
    REMARK = {
        'min_width': '240px',
        'align': 'left'
    }
    DATE_TIME = {
        'min_width': '168px',
        'align': 'left'
    }
    DURATION = {
        'min_width': '200px',
        'align': 'left'
    }
    USER_NAME = {
        'min_width': "148px",
        'align': 'left'
    }
    PASSWORD = {
        'min_width': "200px",
        'align': 'left'
    }
    LINK = {
        'min_width': "140px",
        'align': 'center'
    }
    PORT = {
        'min_width': "102px",
        'align': 'center'
    }
    EMAIL = {
        'min_width': "228px",
        'align': 'left'
    }
    MOBILE = {
        'min_width': "140px",
        'align': 'center'
    }


def showUrl(url):
    if url:
        tag = mark_safe('''<a href="%s" target="blank" class="button" title="%s">URL</a>''' % (url, url))
    else:
        tag = "-"
    return tag


def avatar(url):
    return format_html(
        '''<img src="{}" width="200px" height="100px"  title="点击可浏览" onClick="show_big_img(this)"/>''',
        url, )


class BaseAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY
    date_hierarchy = 'updatedAt'

    def get_fields(self, request, obj=None):
        """
                Hook for specifying fields.
                """
        if self.fields:
            return self.fields
        # _get_form_for_get_fields() is implemented in subclasses.
        form = self._get_form_for_get_fields(request, obj)
        res = [*form.base_fields, *self.get_readonly_fields(request, obj)]
        x = ['remark', 'info']
        for i in x:
            if i in res:
                res.remove(i)
                res.append(i)
        return res

    @staticmethod
    def username(value):
        return f'''<div style="display:flex;">
                            <el-input value="{value}" :disabled="false">
                                <template slot="append">
                                    <el-button style="color:white;border-radius: 0 4px 4px 0;width:40px;display: flex;justify-content: center;align-items: center;" type="primary" icon="el-icon-copy-document" onclick="copyStr('{value}')"></el-button>
                                </template>
                            </el-input>
                        </div>'''

    @staticmethod
    def password(value):
        return f'''<div style="display:flex;">
                                        <el-input value="{value}" :disabled="false" :show-password="true" type="password">
                                            <template slot="append">
                                                <el-button style="color:white;border-radius: 0 4px 4px 0;width:40px;display: flex;justify-content: center;align-items: center;" type="primary" icon="el-icon-copy-document" onclick="copyStr('{value}')"></el-button>
                                            </template>
                                        </el-input>
                        </div>'''

    def shwoUrl(url: str):
        tag = mark_safe('''
                    <a class="ui circular icon red button" href="%s" target="blank">
                        <i class="linkify icon"></i>
                    </a>
            ''' % url)
        return tag

    class Media:

        def __init__(self):
            pass

        css = {
            'all': ()
        }
        js = [
            'js/jquery-3.6.0.min.js',
            'js/clipboardUtil.js',
        ]


class PictureShowAdmin(BaseAdmin):
    def __init__(self, model, admin_site):
        self.list_display = super().list_display + ['_img']
        super().__init__(model, admin_site)

    def _img(self, obj):
        _url = ""
        if hasattr(obj, "originalUrl"):
            _url = obj.originalUrl
        if hasattr(obj, "cover"):
            if hasattr(obj.cover, "originalUrl"):
                _url = obj.cover.originalUrl
        return format_html(
            '''<img src="{}" width="200px" height="100px"  title="{}" onClick="show_big_img(this)"/>''',
            _url, "%s\n%s" %
                  (obj.__str__(), _url)

        )

    _img.short_description = "封面"

    class Media:
        js = (
            'js/jquery-3.6.0.min.js',
            'js/imageUtil.js'
        )
