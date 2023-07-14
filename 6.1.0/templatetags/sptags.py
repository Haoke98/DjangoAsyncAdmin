
import json
import os

from django import template

register = template.Library()

from import_export.admin import ImportExportMixinBase
from simplepro import conf
import simplepro
import simpleui

from django.urls import reverse
from django.utils.safestring import mark_safe


@register.simple_tag(takes_context=True)
def has_import_export(context):
    admin = context.get('cl')
    try:
        context['import_url'] = reverse('admin:%s_%s_%s' % (admin.opts.app_label, admin.opts.model_name, 'import'))
    except:
        pass
    try:
        context['export_url'] = reverse('admin:%s_%s_%s' % (admin.opts.app_label, admin.opts.model_name, 'export'))
    except:
        pass

    return issubclass(admin.__class__, ImportExportMixinBase)


@register.simple_tag(takes_context=True)
def get_display_name(context):
    user = context.get('user')

    if user:
        display = ''

        if hasattr(user, 'first_name') and user.first_name:
            display += user.first_name
        if hasattr(user, 'last_name') and user.last_name:
            display += user.last_name
    if not display:
        display = str(user)
    return display


@register.simple_tag
def get_server_url():
    return conf.get_server_url()


@register.simple_tag
def get_sp_version():
    return simplepro.get_version()


@register.simple_tag
def get_device_id():
    return conf.get_device_id()


@register.simple_tag
def get_simple_version():
    return simpleui.get_version()


@register.simple_tag(takes_context=True)
def test_tag(context):
    print(context)
    fieldset = context.get('fieldset')
    for line in fieldset:
        print(line)
    pass


@register.simple_tag
def get_chart_display():
    from django.conf import settings
    name = 'SIMPLEPRO_CHART_DISPLAY'

    return os.environ.get(name, getattr(settings, name, True))


@register.simple_tag
def get_monitor_display():
    from django.conf import settings
    name = 'SIMPLEPRO_MONIT_DISPLAY'

    return os.environ.get(name, getattr(settings, name, True))


@register.simple_tag
def get_upload_url():
    return reverse('editor_upload')


@register.simple_tag
def is_enable_bawa():
    save_dir = os.path.join(os.getcwd(), 'bawa')
    save_file = os.path.join(save_dir, 'bawa_data.json')
    return os.path.exists(save_file)


@register.simple_tag(takes_context=True)
def get_app_info(context):
    data = {}
    if hasattr(context, 'request'):
        request = context.request
        if hasattr(request, 'model_admin'):
            opts = request.model_admin.opts
            data = {
                "app_label": opts.app_label,
                "model_name": opts.model_name
            }
        return json.dumps(data)
    else:
        return "{}"


@register.simple_tag(takes_context=True)
def get_top_html(context):
    """
    获取顶部显示的html
    """
    return get_admin_html(context, 'top_html')


@register.simple_tag(takes_context=True)
def get_bottom_html(context):
    """
    获取底部显示的html
    """
    return get_admin_html(context, 'bottom_html')


def get_admin_html(context, attr):
    request = context.request
    html = ''
    if hasattr(request, 'model_admin'):
        admin = request.model_admin
        
        key = f'get_{attr}'
        if hasattr(admin, key):
            func = getattr(admin, key)
            html = func(request)
        elif hasattr(admin, attr):
            html = getattr(admin, attr)

    if html:
        html = mark_safe(html)
    return html


@register.simple_tag(takes_context=True)
def get_list_filter_tree_info(context):
    """
    获取admin中的list_filter_tree的信息
    """
    request = context.request
    data = ()
    if hasattr(request, 'model_admin'):
        admin = request.model_admin
        if hasattr(admin, 'get_list_filter_tree'):
            data = admin.get_list_filter_tree(request)
        elif hasattr(admin, 'list_filter_tree'):
            data = admin.list_filter_tree

    return data


@register.simple_tag(takes_context=True)
def get_list_filter_tree_options(context, spec):
    """
    获取admin中的list_filter_tree的数据
    """
    request = context.request
    model_admin = request.model_admin

    field_name = spec.field.attname
    model = spec.field.model
    qs = None
    if hasattr(model_admin, 'get_list_filter_tree_queryset'):
        qs = model_admin.get_list_filter_tree_queryset(request, spec.field.name)
    if not qs:
        qs = model.objects
    parents = qs.filter(**{f"{field_name}__isnull": True})

    options = []
    
    for parent in parents:
        
        children = _get_children_data(qs, field_name, parent)
        option = {
            "value": parent.pk,
            "label": parent.__str__(),
        }
        if children:
            option["children"] = children

        options.append(option)

    return options


def _get_children_data(qs, field_name, parent):
    """
    获取子节点数据
    """
    children = []
    for child in qs.filter(**{f"{field_name}": parent}):
        c = _get_children_data(qs, field_name, child)
        item = {
            "value": child.pk,
            "label": child.__str__(),
        }
        if c:
            item["children"] = c
        children.append(item)
    return children


@register.simple_tag(takes_context=True)
def media_css(context):
    result = []
    css = context.request.model_admin.Media.css
    if css:
        
        if isinstance(css, dict):
            for key, value in css.items():
                if isinstance(value, (list, tuple)):
                    for item in value:
                        result.append(f'<link href="{item}" type="text/css" media="{key}" rel="stylesheet">')
                else:
                    result.append(f'<link href="{value}" type="text/css" media="{key}" rel="stylesheet">')
        else:
            
            for item in css:
                result.append(f'<link href="{item}" type="text/css" rel="stylesheet">')
    return "\n".join(result)
