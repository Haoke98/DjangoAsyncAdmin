import base64
import json
import logging
import os
import re
import time
import traceback
from inspect import isfunction, ismethod

from django.contrib.auth.models import Permission
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import ForeignKey, Model, Q
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

from simplepro.action import BaseAction
from simplepro.components import fields as s_fields
from django.db import models

from simplepro.dialog import BaseDialog

try:
    from django.utils.translation import ugettext as _
except:
    from django.utils.translation import gettext as _

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text
from django.utils.functional import Promise

import datetime


class LazyEncoder(DjangoJSONEncoder):
    """
        解决json __proxy__ 问题
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Promise):
            return force_text(obj)
        return str(obj)


def get_model_fields(model, base=None):
    """
    获取模型的字段，2级
    :param model:
    :param base:
    :return:
    """
    list = []
    fields = model._meta.fields
    for f in fields:
        label = f.name
        if hasattr(f, 'verbose_name'):
            label = getattr(f, 'verbose_name')

        if isinstance(label, Promise):
            label = str(label)
        temp_class = None
        if hasattr(f, '__class__'):
            temp_class = str(f.__class__.__name__)
        if base:
            list.append(('{}__{}'.format(base, f.name), label, temp_class))
        else:
            list.append((f.name, label, temp_class))

    return list


def find_field(fields, name):
    for k in fields:
        if name == k[0]:
            return k
    return False


MODEL_CACHE = {}


def get_model_headers(model_admin, request):
    """
    custom model admin headers
    """

    list_display = model_admin.get_list_display(request)

    fun_fields = []
    values_fields = []
    headers = []

    fields = get_model_fields(model_admin.model)

    fields_options = {}
    if hasattr(model_admin, 'fields_options'):
        fields_options = getattr(model_admin, 'fields_options')

    for i in list_display:
        field = find_field(fields, i)
        if field:
            label = field[1]
            values_fields.append(i)
            d = {
                'name': i,
                'label': label
            }
            if i in fields_options:
                d = dict(d, **fields_options.get(i))

            if 'sortable' not in d:
                d['sortable'] = 'custom'
            d['type'] = field[2]

            if field[2] == 'AMapField':
                for f in model_admin.model._meta.fields:
                    if f.name == field[0]:
                        d['apiKey'] = f.params.get('api_key')
                        d['pickType'] = f.params.get('pick_type')

            headers.append(d)

        else:
            fun_fields.append(i)
            label = i

            if hasattr(model_admin, i):
                dt = getattr(model_admin, i).__dict__
            else:
                field = getattr(model_admin.model, i)
                if hasattr(field, '__dict__'):
                    dt = field.__dict__
                else:
                    dt = {}
            if 'short_description' in dt:
                label = dt.get('short_description')
            elif label == '__str__':
                label = model_admin.model._meta.verbose_name_plural
            d = {
                'name': i,
                'label': label
            }
            if i in fields_options:
                d = dict(d, **fields_options.get(i))

            if 'admin_order_field' in dt:
                admin_order_field = dt.get('admin_order_field')
                d['sortable'] = 'custom'
                d['admin_order_field'] = admin_order_field
            else:
                d['sortable'] = False
            d['type'] = 'fun'
            headers.append(d)

    return values_fields, fun_fields, headers


def get_model_info(model_admin, request):
    """
    获取模型信息
    """

    key = str(model_admin)
    if key in MODEL_CACHE:
        cache = MODEL_CACHE.get(key)
        return cache.get('formatter'), cache.get('choices')

    formatter = None
    if hasattr(model_admin, 'formatter'):
        formatter = getattr(model_admin, 'formatter')

    model = model_admin.model
    choices = {}
    for c in dir(model):
        if c.endswith('choices'):
            temp = {}
            array_list = getattr(model, c)
            for i in array_list:
                temp[i[0]] = i[1]
            choices[c] = temp
    for c in model._meta.fields:
        temp = {}
        if hasattr(c, 'choices'):
            if c.choices and len(c.choices) > 0:
                for i in c.choices:
                    temp[i[0]] = i[1]
                choices[c.name] = temp
    MODEL_CACHE[key] = {
        'formatter': formatter,
        'choices': choices,
    }
    return formatter, choices


def get_layer_url(admin):
    """
    获取url配置
    """
    try:
        opts = admin.opts
        key = "admin:{}_{}_layer".format(opts.app_label, opts.model_name)
    except Exception:

        logging.warning(f"使用异步获取layer配置，需要让Admin继承AjaxAdmin")
        print(f"使用异步获取layer配置，需要让Admin继承AjaxAdmin")
        traceback.print_exc()
    return reverse(key)


def get_custom_button(request, admin):
    data = {}
    actions = admin.get_actions(request)

    app_label = admin.opts.app_label
    if actions:
        id = 0
        for name in actions:
            values = {}
            fun = actions.get(name)[0]
            for key, v in fun.__dict__.items():
                if key != '__len__' and key != '__wrapped__':
                    if key == 'layer' and isfunction(v):

                        values['layer'] = {
                            'is_fun': True,
                            'url': get_layer_url(admin)
                        }
                    else:
                        values[key] = v
            values['eid'] = id
            id += 1
            if name == 'export_admin_action':
                values['label'] = '选中导出'
                values['isExport'] = True
                values['icon'] = 'el-icon-finished'
                formats = []
                for i in enumerate(admin.get_export_formats()):
                    formats.append({
                        'value': i[0],
                        'label': i[1]().get_title()
                    })

                values['formats'] = formats
            else:
                values['label'] = actions.get(name)[2]

            if not request.user.is_superuser:
                exists = Permission.objects.filter(codename=name, content_type__app_label=app_label,
                                                   content_type__model=admin.opts.model_name).exists()
                if exists:
                    if request.user.has_perm('{}.{}'.format(app_label, name)):
                        data[name] = values
                else:
                    data[name] = values
            else:
                data[name] = values
    if 'delete_selected' in data:
        del data['delete_selected']
    return data


def search_placeholder(cl):
    fields = get_model_fields(cl.model)

    for f in cl.model._meta.fields:
        if isinstance(f, ForeignKey):
            fields.extend(get_model_fields(f.related_model, f.name))

    verboses = []

    for s in cl.search_fields:
        for f in fields:
            if f[0] == s:
                verboses.append(f[1])
                break

    return ",".join(verboses)


def write(data, msg='ok', state=True):
    rs = {
        'state': state,
        'msg': msg,
        'data': data
    }

    return HttpResponse(json.dumps(rs, cls=LazyEncoder), content_type='application/json')


def write_obj(obj):
    return HttpResponse(json.dumps(obj, cls=LazyEncoder), content_type='application/json')


def has_permission(request, admin, permission):
    codename = get_permission_codename(permission, admin.opts)
    key = '{}.{}'.format(admin.opts.app_label, codename)

    return request.user.has_perm(key)


def get_permission_codename(action, opts):
    """
    Return the codename of the permission for the specified action.
    """
    return '%s_%s' % (action, opts.model_name)


from simpleui.templatetags import simpletags
from simpleui.templatetags.simpletags import get_config


def get_menus(request, admin_site):
    """
    获取自定义菜单的权限，内置菜单不处理权限
    :param request:
    :param admin:
    :return:
    """
    context = {
        'app_list': admin_site.get_app_list(request),
        'request': request
    }

    def has_perm(key):
        return request.user.has_perm(key)

    def _filter(menus, is_append=True):
        temps = []
        for item in menus:
            codename = item.get('codename')

            if 'codename' in item:

                key = '{}.{}'.format(item.get('name'), codename)

                if has_perm(key):
                    if 'models' in item:
                        item['models'] = _filter(item['models'], is_append=False)
                    temps.append(item)
            else:

                temps.append(item)
        return temps

    def _get_config(key):
        _config = get_config(key)
        if key == 'SIMPLEUI_CONFIG':

            _config = get_config(key)
            if _config and 'menus' in _config:
                menus = _config.get('menus')
                _config['menus'] = _filter(menus)
        return _config

    return simpletags.menus(context, _get_config=_get_config)


def trans_permission_name(t):
    """
    处理国际化显示
    """
    name = t.name
    ct = t.content_type
    pname = name
    if 'Can add' in name:
        pname = _("Can add")
    elif 'Can change' in name:
        pname = _("Can change")
    elif 'Can delete' in name:
        pname = _("Can delete")
    elif 'Can view' in name:
        pname = _("Can view")

    return f'{pname}{ct.name}'


def init_permissions():
    """
   初始化权限显示方式，更加友好
   """
    from django.contrib.auth.models import Permission
    Permission.__str__ = lambda t: '%s' % (trans_permission_name(t))


def get_checkbox_field_value(field, value):
    """
    checkbox的字段 特殊显示
    """

    if value and hasattr(field, 'items'):
        items = getattr(field, 'items')
        split_values = value.split(',')
        new_value = []
        for v in split_values:
            for item in items:
                if str(item[0]) == str(v):
                    new_value.append(item[1])
        return new_value

    else:
        return value


def get_model_pk(model):
    return 'pk'


def process_search_fields(request, model_admin, queryset):
    """
    处理搜索字段
    """
    search = request.POST.get('search')
    if search and search != '':
        q = Q()
        search_fields = model_admin.search_fields
        for s in search_fields:
            q = q | Q(**{s + "__icontains": search})
        try:
            queryset = queryset.filter(q)
        except Exception as e:
            traceback.print_exc()
            raise e
    return queryset


def process_page(request, model_admin, queryset):
    """
    处理分页
    """
    current_page = request.POST.get('current_page')
    if current_page:
        current_page = int(current_page)
    else:
        current_page = 1

    page_size = model_admin.list_per_page
    if 'page_size' in request.POST:
        r = int(request.POST.get('page_size'))
        if r != 0:
            page_size = r

    page = Paginator(queryset, page_size)
    if current_page > page.num_pages:
        current_page = page.num_pages
    return page.page(current_page), page_size


def process_order_by(request, qs):
    """
    处理排序
    """
    if 'order_by' in request.POST:
        field_name = request.POST.get('order_by')
        if field_name and field_name != '' and field_name != 'null':
            qs = qs.order_by(field_name)

    if hasattr(qs, 'ordered') and not qs.ordered:
        qs = qs.order_by('-pk')
    return qs


def get_boolean_fields(model_admin):
    boolean_fields = []
    fields = model_admin.model._meta.get_fields()
    for field in fields:
        if isinstance(field, models.BooleanField):
            boolean_fields.append(field.name)
    return boolean_fields


def is_boolean_field(field_name, boolean_fields):
    temp = field_name.split('__')[0]
    return temp in boolean_fields


def get_filter(request, model_admin, queryset):
    """
    获取过滤条件
    """

    query = {}
    filters = request.POST.get('filters')
    if filters and filters != '':
        filters = json.loads(filters)

        between_fields = get_admin_property(model_admin, request, 'between_fields')
        if not between_fields:
            between_fields = []

        for key in filters:

            if key in between_fields:
                value = filters.get(key)
                if value and len(value) == 2:
                    val1 = value[0]
                    val2 = value[1]
                    if val1 and val1 != '':
                        query['{}__gte'.format(key)] = val1
                    if val2 and val2 != '':
                        query['{}__lte'.format(key)] = val2

            elif key in model_admin.filter_mappers:

                _filter = model_admin.filter_mappers[key]
                _filter.used_parameters = filters

                queryset = _filter.queryset(request, queryset)
            else:

                if key not in filters:
                    print("过滤字段不存在，请清理浏览器缓存")
                    continue

                val = filters.get(key)
                if is_boolean_field(key, get_boolean_fields(model_admin)):
                    r = val.upper() == 'TRUE'
                    query[key.replace('__exact', '')] = r

                elif type(val) is int:
                    query[key.replace('__exact', '')] = val
                elif type(val) == tuple or type(val) == list:
                    query[key.replace('__exact', '__in')] = val
                elif type(val) is str:

                    if re.fullmatch(r'\d{4}\-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}\s\d{2}\:\d{2}', val):
                        t = re.match(r'\d{4}\-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}', val)
                        if t:
                            temp = t[0]
                            date = datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S')
                            val = date + datetime.timedelta(hours=8)
                    elif re.fullmatch(r'\d{4}\-\d{2}-\d{2}\s\d{2}\:\d{2}\:\d{2}', val):

                        val = datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                    elif re.fullmatch(r'\d{4}\-\d{2}-\d{2}', val):

                        val = datetime.datetime.strptime(val, '%Y-%m-%d')
                    elif re.fullmatch(r'\d{3}\-\d{2}-\d{2}', val):

                        val = time.strptime(val, ' %H:%M:%S')
                    query[key] = val

    return query, queryset


def get_cell(object_list, model_admin, request):
    rows = []
    formatter, choices = get_model_info(model_admin, request)
    values_fields, fun_fields, headers = get_model_headers(model_admin, request)

    list_display_links = ()
    if hasattr(model_admin, 'list_display_links'):
        list_display_links = model_admin.list_display_links

    if not list_display_links:
        list_display_links = ()

    for bean in object_list:
        row = {}
        for field_name in values_fields:
            key = field_name + '_choices'
            if key in choices:
                value = getattr(bean, field_name)
                mappers = choices[key]
                if value in mappers:
                    value = mappers.get(value)

            elif field_name in choices:
                value = getattr(bean, field_name)
                mappers = choices[field_name]
                if value in mappers:
                    value = mappers.get(value)
            else:

                model = model_admin.model
                value = getattr(bean, field_name)
                if hasattr(model, field_name):
                    tmp = getattr(model, field_name)
                    if hasattr(tmp, 'field'):
                        field = tmp.field
                        if isinstance(field, s_fields.CheckboxField):
                            value = get_checkbox_field_value(field, value)
                if value and issubclass(value.__class__, models.fields.files.ImageFieldFile):
                    value = format_html(
                        '<a href="{}" target="_blank"><img src="{}" alt="{}" style="max-height:100%;max-width:100%"></a>',
                        value.url, value.url, value)

            if formatter:
                value = formatter(bean, field_name, value)
            elif issubclass(value.__class__, Model):

                if hasattr(value, '__unicode__'):
                    value = value.__unicode__()
                else:
                    value = str(value)

            if field_name in list_display_links and not formatter:
                opts = model_admin.opts
                url = reverse('admin:{}_{}_changelist'.format(opts.app_label, opts.model_name))
                pk_field = get_model_pk(model_admin.model)
                _id = getattr(bean, pk_field)
                url = url + '{}/change'.format(_id)
                value = format_html('<a href="{}">{}</a>', url, str(value))

            if value is None or value == "" and hasattr(model_admin, 'get_empty_value_display'):
                value = model_admin.get_empty_value_display()
                if value == '-':
                    value = ""
            row[field_name] = value

        for f in fun_fields:
            try:
                if f == '__str__':
                    if hasattr(model_admin.model, '__str__'):
                        value = getattr(model_admin.model, '__str__')(bean)
                    else:
                        value = None

                elif hasattr(model_admin, f):

                    value = getattr(model_admin, f)
                    if isfunction(value) or ismethod(value):
                        value = value.__call__(bean)
                    elif isinstance(value, property):
                        value = value.fget(bean)
                elif f == 'pk':
                    value = getattr(bean, f)
                else:
                    value = getattr(model_admin.model, f)
                    if isfunction(value) or ismethod(value):
                        value = value.__call__(bean)
                    elif isinstance(value, property):
                        value = value.fget(bean)

                value = get_dialog_value(value)
                if formatter:
                    value = formatter(bean, f, value)
                row[f] = value
            except Exception as e:
                traceback.print_exc()

                if hasattr(f, ' __qualname__'):
                    raise Exception(
                        e.args[0] + '\n call {} error. 调用自定义方法出错，请检查模型中的{}方法'.format(f.__qualname__,
                                                                                     f.__qualname__))
                else:
                    raise e

        pk_field = get_model_pk(model_admin.model)
        row['_id'] = getattr(bean, pk_field)
        rows.append(row)
    return rows


def get_dialog_value(fn_value):
    if isinstance(fn_value, BaseDialog) or isinstance(fn_value, BaseAction):
        return fn_value.to_dict()
    else:
        return fn_value


def offline_active_code(data):
    """
    离线激活模式
    """
    lic_file = os.path.join(os.getcwd(), 'simplepro.lic')
    f = open(lic_file, 'wb')
    f.seek(0)
    byte = base64.b64decode(data)
    f.write(byte)
    f.close()


def is_display_tree_table(model_admin, request):
    """
    是否显示树形表格
    :param model_admin:
    :return:
    """
    return get_admin_property(model_admin, request, 'list_display_tree_cascade') is not None


def get_admin_tree_info(model_admin, request):
    """
    获取树形表格的信息
    """
    tree_field_name = get_admin_property(model_admin, request, 'list_display_tree_cascade')

    return tree_field_name, get_admin_property(model_admin, request, 'list_display_tree_expand_all')


def get_admin_property(model_admin, request, name):
    """
    获取admin的属性，入参只能是request
    """
    fun_name = f'get_{name}'
    if hasattr(model_admin, fun_name):
        return getattr(model_admin, fun_name)(request)
    elif hasattr(model_admin, name):
        return getattr(model_admin, name)


def get_tree_data(qs, rows, tree_field_name, model_admin, request):
    """
    获取树形数据
    """
    for row in rows:
        row['children'] = get_table_tree_children(qs, row, tree_field_name, model_admin, request)

    return rows


def get_table_tree_children(qs, item, tree_field_name, model_admin, request):
    """
    获取树形子节点
    """

    children = qs.filter(**{tree_field_name: item['_id']})
    if children:
        _rows = get_cell(children, model_admin, request)
        for _row in _rows:
            _children = get_table_tree_children(qs, _row, tree_field_name, model_admin, request)
            _row['children'] = _children
        return _rows


def get_table_show_selection(model_admin, request):
    """
    是否显示选择框
    """
    show_selection = get_admin_property(model_admin, request, 'show_selection')
    if show_selection is None:
        show_selection = True
    return show_selection


def get_admin_dynamic_render(model_admin, request, queryset):
    """
    获取动态渲染的字段
    """
    if hasattr(model_admin, 'get_dynamic_render'):
        try:
            r = model_admin.get_dynamic_render(request, queryset)
        except Exception as e:
            raise Exception(f'{str(model_admin.__module__)}.{model_admin.__class__.__qualname__} Error:', e)
        return r
