import datetime
import json
import os
import struct
import traceback

import requests
import rsa as rsa
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.admin import GroupAdmin
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from simplepro import conf
from .bawa import views as bawa_views

try:
    from django.utils.translation import ugettext as _
except:
    from django.utils.translation import gettext as _

from simplepro.utils import LazyEncoder, write, search_placeholder, get_custom_button, \
    get_menus, write_obj, get_model_headers, get_model_pk, get_cell, get_filter, \
    process_search_fields, process_order_by, process_page, is_display_tree_table, get_admin_tree_info, get_tree_data, \
    get_table_show_selection, get_admin_dynamic_render

URL_CACHE = {}

import base64

cache_d = None

lic_file = os.path.join(os.getcwd(), 'simplepro.lic')

from django.forms import fields, models as form_models


def O0O0OOO0OOO0OO0O0(reload=False):
    try:

        if not os.path.exists(lic_file):
            return False
        global cache_d
        if reload:
            cache_d = None

        if cache_d:
            return cache_d
        f = open(lic_file, 'rb')
        buffer = f.read()
        a, = struct.unpack('h', buffer[0:2])
        b, = struct.unpack('h', buffer[2:4])
        d1 = buffer[4:a + 4]
        d2 = base64.b64decode(buffer[a + 4:a + 4 + b])

        # 文件被改动移动过

        # decode
        pk = rsa.PrivateKey.load_pkcs1(d2)
        text = rsa.decrypt(d1, pk).decode()  # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str
        d = json.loads(text)
        cache_d = d
    except Exception as e:
        pass
    return d


def OO0O0OO0OOO0OO0O0(request):
    try:
        d = O0O0OOO0OOO0OO0O0()
        # 校验失效时间和设备ID
        end = d.get('end_date').split(' ')[0]
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
        now = datetime.datetime.now()
        if now > end_date:
            request.msg = '您的激活码已于<strong>{}<strong>过期，请重新购买！'.format(end_date)
            return False
        device_id = d.get('device_id')
        if str(conf.get_device_id()) != str(device_id):
            request.msg = '激活码和设备ID不匹配，请重新激活！<div>您的设备ID:{}</div><div>激活的设备ID:{}</div>'.format(
                conf.get_device_id(),
                device_id)
            return False
        return True
    except Exception as e:
        # raise e
        pass
    return False


def pre_process(request, view_func):
    # 如果不是admin的url，不拦截
    admin_url = reverse('admin:index')
    if hasattr(view_func, 'admin_site'):
        # 如果是admin 直接过，普通用户才做权限处理
        if request.user and not request.user.is_superuser:
            request.menus = get_menus(request, view_func.admin_site)

    if not hasattr(view_func, 'model_admin') or request.path.find(admin_url) == -1:
        return None

    # 如果admin中有 native_render 就不处理，用simpleui渲染
    if hasattr(view_func.model_admin, 'native_render') and view_func.model_admin.native_render:
        return

    # 刷新的参数移除_，防止报错
    if '_' in request.GET:
        if hasattr(request.GET, '_mutable'):
            request.GET._mutable = True
            del request.GET['_']

    if not OO0O0OO0OOO0OO0O0(request):
        return process_active(request)

    # 如果是is_popup 不处理
    if '_popup' in request.GET or not request.user.is_authenticated:
        pass
    elif 'model_admin' in view_func.__dict__:

        # 把admin直接加入到request，让后续的自定义标签一类，可以直接访问admin
        request.model_admin = view_func.model_admin

        if isinstance(view_func.model_admin, GroupAdmin):
            class Media:
                js = ('admin/group/js/group.js',)

            view_func.model_admin.Media = Media
            view_func.model_admin.list_display = ('id', 'name')
            view_func.model_admin.list_per_page = 10
        path = request.path

        opts = view_func.model_admin.opts
        key = 'admin:{}_{}_changelist'.format(opts.app_label, opts.model_name)
        # model_admin

        temp = URL_CACHE.get(path)
        if temp:
            return process_list(request, temp)

        elif reverse(key) == path:
            # 加入缓存提示性能
            URL_CACHE[request.path] = view_func.model_admin
            return process_list(request, view_func.model_admin)


def custom_action(request, model_admin):
    """处理自定义按钮的动作"""
    """
        默认，执行成功就会返回成功，失败就失败，如果用户自己有返回数据，就用用户返回的
    """

    rs = {
        'state': True,
        'msg': '操作成功！',
    }
    try:
        post = request.POST

        _all = post.get('all')
        ids = post.get('ids')
        key = post.get('key')
        filters = post.get('filters')

        """
        action: "custom_action"
        all: 0
        ids: "102,100"
        key: "make_copy"""
        model = model_admin.model
        queryset = model.objects.get_queryset()

        # 处理默认查询条件
        query = {}
        if _all == '0':
            if ids:
                query[get_model_pk(model) + '__in'] = ids.split(',')

        if filters:
            _filters, qs = get_filter(request, model_admin, queryset)
            queryset = queryset.filter(**_filters)

        queryset = queryset.filter(**query)

        fun = getattr(model_admin, key)
        result = fun(request, queryset)
        if isinstance(result, HttpResponseRedirect):
            return JsonResponse(data={
                "state": True,
                "type": "redirect",
                "url": result.url
            })
        # 允许自己返回参数，必须是词典才行
        if result and isinstance(result, dict):
            rs = result

        # 如果result 是None的时候，就读取自定义的message
        if result is None:
            rs = {
                'state': True,
                'messages': []
            }
            ms = messages.get_messages(request)
            for item in ms:
                rs['messages'].append({
                    'msg': item.message,
                    'tag': item.level_tag,
                })

    except Exception as e:
        rs = {
            'state': False,
            'msg': e.args[0]
        }
        traceback.print_exc()

    return HttpResponse(json.dumps(rs, cls=LazyEncoder), content_type='application/json')


def process_list(request, model_admin):
    """
    处理列表数据，ajax请求
    """
    if '_editor' in request.GET:
        return process_editor(request)

    action = request.POST.get('action')

    actions = {
        'list': list_data,
        'delete': delete_data,
        # 自定义按钮
        'custom_action': custom_action,
        'modify': list_modify,
    }

    if action and action not in actions:
        pass
    elif action:
        # 自定义filter做映射
        filter_mappers = {}
        changelist = model_admin.get_changelist_instance(request)
        if changelist.has_filters:
            for spec in changelist.filter_specs:
                param_name = None
                if hasattr(spec, 'field_path'):
                    param_name = spec.field_path
                elif hasattr(spec, 'parameter_name'):
                    param_name = spec.parameter_name
                elif hasattr(spec, 'lookup_kwarg'):
                    param_name = spec.lookup_kwarg
                if param_name:
                    filter_mappers[param_name] = spec
        model_admin.filter_mappers = filter_mappers
        try:
            return actions[action](request, model_admin)
        except Exception as e:
            traceback.print_exc()
            return write(data=None, msg=e.args[0], state=False)

    else:

        # 响应搜索参数
        # 判断是否有查看页面的权限
        if not model_admin.has_view_permission(request):
            return no_permission(request)

        changelist = model_admin.get_changelist_instance(request)
        model_admin.has_filters = changelist.has_filters
        model_admin.filter_specs = changelist.filter_specs
        searchModel = []
        if model_admin.has_filters:
            for spec in model_admin.filter_specs:
                # parameter_name
                if hasattr(spec, 'field_path'):
                    searchModel.append(spec.field_path)
                elif hasattr(spec, 'parameter_name'):
                    searchModel.append(spec.parameter_name)
                elif hasattr(spec, 'lookup_kwarg'):
                    searchModel.append(spec.lookup_kwarg)

        # 解析Media
        media = None

        if hasattr(model_admin, 'Media'):
            m = model_admin.Media
            media = {}
            if hasattr(m, 'js'):
                new_array = []
                # 移除导入导出插件的js
                jss = getattr(m, 'js')

                for js in jss:
                    if not js.endswith('import_export/action_formats.js'):
                        new_array.append(js)

                media['js'] = new_array
            if hasattr(m, 'css'):
                media['css'] = getattr(m, 'css')

        # 获取3个权限
        # has_delete_permission
        # has_add_permission
        # has_change_permission

        # 如果有messages，就获取，然后在页面进行显示

        mlist = []
        ms = messages.get_messages(request)
        for item in ms:
            mlist.append({
                'msg': str(item.message),
                'tag': str(item.level_tag),
            })

        list_filter_multiples = []

        if hasattr(model_admin, 'get_list_filter_multiples'):
            list_filter_multiples = model_admin.get_list_filter_multiples(request)

        elif hasattr(model_admin, 'list_filter_multiples'):
            list_filter_multiples = getattr(model_admin, 'list_filter_multiples')

        # 获取post参数，
        template_name = 'admin/results/list.html'
        if hasattr(model_admin, 'change_list_template') and getattr(model_admin, 'change_list_template'):
            temp = getattr(model_admin, 'change_list_template')
            if "import_export/change_list_import.html" not in temp and 'import_export/change_list_export.html' not in temp and "import_export/change_list_import_export.html" not in temp:
                template_name = temp

        # 兼容django-import-export 引发的错误
        # allow_error_import_export(model_admin, request)

        return render(request, template_name, {
            'request': request,
            'cl': model_admin,
            'opts': model_admin.opts,
            'media': media,
            'title': model_admin.model._meta.verbose_name_plural,
            'model': model_admin.model,
            'searchModels': json.dumps(searchModel, cls=LazyEncoder),
            # 'has_delete_permission': has_permission(request, model_admin, 'delete'),
            # 'has_add_permission': has_permission(request, model_admin, 'add'),
            # 'has_change_permission': has_permission(request, model_admin, 'change'),
            'has_delete_permission': model_admin.has_delete_permission(request),
            'has_add_permission': model_admin.has_add_permission(request),
            'has_change_permission': model_admin.has_change_permission(request),
            'mlist': json.dumps(mlist),
            # 多选
            'list_filter_multiples': list_filter_multiples,
            'has_summaries': hasattr(model_admin, 'get_summaries'),
            'has_editor': get_has_editor(model_admin),
        })


def no_permission(request):
    html = render_to_string('admin/permissions/no_permission.html', {
        'msg': _("do not have permission")
    })
    return HttpResponse(status=403, content=html)


def get_has_editor(admin):
    # TODO 还得有权限
    return len(admin.list_editable) != 0


def list_modify(request, admin):
    """
    列表字段编辑
    """
    # 判断是否有修改数据的权限
    if not admin.has_change_permission(request):
        return write_obj({
            'state': False,
            'msg': _('Sorry, you do not have permission')
        })

    post = request.POST
    rs = {
        'state': True,
        'msg': _('Modify the success')
    }
    field = post.get('field')
    value = post.get('value')

    # 修改数据
    try:
        obj = admin.get_object(request, post.get('pk'))
        # 给字段设置值
        setattr(obj, field, value)
        obj.save()

    except Exception as e:

        rs = {
            'state': False,
            'msg': _('Modify the failure') + e.args[0]
        }

    return write_obj(rs)


def delete_data(request, model_admin):
    """
    删除数据
    :param request:
    :return:
    """
    # 判断是否有删除数据的权限
    if not model_admin.has_delete_permission(request):
        return write_obj({
            'state': False,
            'msg': _('Sorry, you do not have permission')
        })

    # 拼凑queryset
    model = model_admin.model
    _queryset = model.objects.get_queryset()
    ids = request.POST.get('ids')

    rs = {
        'state': True,
        'msg': _('Deleted successfully')
    }
    qs = _queryset
    if request.POST.get('all') == '1':
        query, qs = get_filter(request, model_admin, _queryset)
        qs = qs.filter(**query)
    # 处理搜索字段
    qs = process_search_fields(request, model_admin, qs)
    if ids:
        ids = ids.split(',')
        qs = qs.filter(pk__in=ids)

    try:

        for obj in qs:
            obj_display = str(obj)
            # 记录下日志
            model_admin.log_deletion(request, obj, obj_display)
        model_admin.delete_queryset(request, qs)

    except Exception as e:
        rs = {
            'state': False,
            'msg': _('Delete failed') + e.args[0]
        }
    return write(rs)


def list_data(request, model_admin):
    """
    获取list数据
    :param request:
    :param model_admin:
    :return:
    """
    """
        admin 中字段设置
        fields_options={
            'id':{
                'fixed':'left',
                'width':'100px',
                'algin':'center'
            }
        }
    """
    # 判断是否有查看页面的权限

    if not model_admin.has_view_permission(request):
        return no_permission(request)

    table = {}

    # values_fields,fun_fields,headers 缓存
    values_fields, fun_fields, headers = get_model_headers(model_admin, request)

    # queryset是从admin中获取
    queryset = model_admin.get_queryset(request)

    # 处理q
    queryset = process_search_fields(request, model_admin, queryset)

    # 处理过滤
    query, queryset = get_filter(request, model_admin, queryset)

    # 过滤数据
    qs = queryset.filter(**query)

    # 树形表格
    is_tree_table = is_display_tree_table(model_admin, request)
    tree_field_name = None
    tree_expand_all = False

    if is_tree_table:
        tree_field_name, tree_expand_all = get_admin_tree_info(model_admin, request)
        # 过滤数据，只显示根节点
        qs = qs.filter(**{f"{tree_field_name}__isnull": True})

    # 处理排序
    qs = process_order_by(request, qs)

    # 处理分页
    page, page_size = process_page(request, model_admin, qs)

    # 获取数据
    rows = get_cell(page.object_list, model_admin, request)
    if is_tree_table:
        new_qs = model_admin.get_queryset(request)
        rows = get_tree_data(new_qs, rows, tree_field_name, model_admin, request)
    # 根据需要的字段进行返回

    table['headers'] = headers

    # 处理统计
    if hasattr(model_admin, 'get_summaries'):
        table['summaries'] = model_admin.get_summaries(request, qs)

    # 第二页开始就不返回headers
    initialized = request.POST.get('initialized')
    if initialized != 'true':
        actions_show = True
        if hasattr(model_admin, 'actions_show'):
            actions_show = getattr(model_admin, 'actions_show') is True
        # table['headers'] = headers
        table['exts'] = {
            'showId': 'id' in values_fields,
            'actions_show': actions_show,
            'showSearch': len(model_admin.search_fields) > 0,
            'search_placeholder': search_placeholder(model_admin),
            'showSelection': get_table_show_selection(model_admin, request),
        }

        if is_tree_table:
            table['exts']['treeTable'] = {
                'expandAll': tree_expand_all,
                'treeField': tree_field_name
            }

        # 获取自定义按钮
        table['custom_button'] = get_custom_button(request, model_admin)

    # 如果admin中有get_results方法，将使用get_results的返回的数据
    if hasattr(model_admin, 'get_results'):
        rows = model_admin.get_results(rows, request, queryset)

    table['rows'] = rows
    table['paginator'] = {
        'page_size': page_size,
        'count': page.paginator.count,
        'page_count': page.paginator.num_pages

    }
    # 自6.5+ 开始支持页面动态渲染内容
    table['dynamic_display'] = get_admin_dynamic_render(model_admin, request, queryset)

    return write(table)


def process_active(request):
    # 如果是ajax就返回错误信息，是页面就返回页面
    rules = [reverse('admin:index'), reverse('admin:login'), reverse('admin:logout')]
    path = request.path

    post = request.POST
    action = post.get('action')
    if action:
        return write(None, _('Not activated, please contact customer service staff to activate!'), False)
    elif path not in rules:
        return render(request, 'admin/active.html', {
            'device_id': conf.get_device_id()
        })


def online_active_code(code):
    """
    在线激活模式
    """
    device_id = conf.get_device_id()

    url = conf.get_server_url() + '/active'
    r = requests.post(url, data={
        'device_id': device_id,
        'active_code': code
    })

    if r.status_code == 200:
        data = r.json()
        if data.get('state') is True:
            # 获取根目录，写入激活文件
            # 内容需要混淆写入

            f = open(lic_file, 'wb')

            # d1 = bytes(data.get('license'), encoding='utf8')
            d1 = base64.b64decode(data.get('license'))
            d2 = base64.b64encode(bytes(data.get('private_key'), encoding='utf8'))

            f.write(struct.pack('h', len(d1)))
            f.write(struct.pack('h', len(d2)))

            f.write(d1)
            f.write(d2)

            f.close()
            O0O0OOO0OOO0OO0O0(True)

            # pass
        return write_obj(data)


def process_lic(request):
    # 调用服务器接口，获取激活信息，如果激活成功，就覆盖本地文件
    active_code = request.POST.get('active_code')

    r = online_active_code(active_code)
    if r:
        return r
    return write({}, 'error', False)


def process_info(request):
    return render(request, 'admin/active.html', {
        'page_size': OO0O0OO0OOO0OO0O0(request),
        'data': O0O0OOO0OOO0OO0O0(),
        'device_id': conf.get_device_id()
    })


def process_package(request):
    r = requests.get("{}/package".format(conf.get_server_url()))
    return write(r.json())


def pre_reload(request):
    if hasattr(request, 'reload'):
        O0O0OOO0OOO0OO0O0(True)


def process_editor(request):
    pk = request.GET.get('_pk')

    admin = request.model_admin
    model = admin.model
    ins = model.objects.get(pk=pk)
    data = None

    class GeneralForm(ModelForm):

        class Meta:
            model = admin.model
            fields = admin.list_editable

    if request.method == 'GET':
        form = GeneralForm(instance=ins)
    else:
        form = GeneralForm(data=request.POST, instance=ins)
        if form.is_valid():
            obj = form.save()
            data = {
                'state': True,
                'msg': _('Successfully')
            }
            # 调用admin的信号
            admin.save_form(request, form, True)
            # 调用save model
            admin.save_model(request, obj, form, True)

        else:
            data = {
                'state': False,
                'msg': _('Failed')
            }
    # http://localhost:8000/demo/employe/?_editor=1&_pk=4
    if data:
        data = json.dumps(data)

    # 每个字段获取类型
    types = {}

    for name in form.fields:
        field = form.fields.get(name)
        if issubclass(type(field), fields.ChoiceField) or issubclass(type(field),
                                                                     form_models.ChoiceField) or issubclass(type(field),
                                                                                                            form_models.ModelChoiceField):
            types[name] = 'select'
        elif issubclass(type(field), fields.BooleanField):
            types[name] = 'boolean'
        elif issubclass(type(field), fields.DateField):
            types[name] = 'date'
        elif issubclass(type(field), fields.TimeField):
            types[name] = 'time'
        elif issubclass(type(field), fields.DateTimeField):
            types[name] = 'datetime'

    return render(request, 'admin/results/editor.html', {
        'form': form,
        'types': json.dumps(types),
        'data': data
    })


def process_models(request):
    rs = []
    session = request.session
    if '_menus' in session:
        temp = session.get('_menus')

        temp_obj = json.loads(temp)

        for item in temp_obj:
            rs.append({
                'name': item.get('name'),
                'icon': item.get('icon'),
                'url': item.get('url')
            })

            if 'models' in item:
                ms = item.get('models')
                for sub in ms:
                    rs.append({
                        'name': sub.get('name'),
                        'icon': sub.get('icon'),
                        'url': sub.get('url')
                    })

    response = HttpResponse(json.dumps(rs), content_type='application/json')
    # response['Access-Control-Allow-Methods'] = '*'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


def bawa_page(request):
    # 使用拦截器 拦截所有的bawa页面，作用是 session问题
    if 'bawa/data' in request.path:
        return bawa_views.get_data(request)
    elif 'bawa/save' in request.path:
        return bawa_views.save(request)
    # 如果项目内用默认的图表url
    elif '.json' in request.path:
        return redirect(settings.STATIC_URL + request.path.replace('/sp', '/admin'))
    else:
        return render(request, 'admin/bawa/render.html')