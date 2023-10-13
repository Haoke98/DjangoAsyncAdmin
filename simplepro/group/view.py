from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from simplepro.utils import write
from .utils import get_permissions
from .. import utils


def action(request):
    _action = request.POST.get('action')
    if not _action:
        return HttpResponse('非法请求', status=403)

    mappers = {
        'tree': get_tree,
        'save': save,
        'get_detail': get_detail
    }

    return mappers.get(_action)(request)


def get_detail(request):
    id = request.POST.get('id')
    r = Group.objects.filter(id=id).first()
    ids = []
    if r:
        all = r.permissions.all()
        for item in all:
            ids.append(item.id)

    return write(ids)


def save(request):
    state = True
    msg = "ok"
    try:
        name = request.POST.get('name')
        ids = request.POST.get('ids')
        id = request.POST.get('id')

        if id and id != '':
            group = Group.objects.get(id=id)

            group.permissions.clear()
        else:
            group = Group.objects.create(name=name)
        if ids and ids != '':
            ids = ids.split(',')
            for i in ids:
                group.permissions.add(i)
    except Exception as e:
        state = False
        msg = e.args[0]
    return write(None, msg, state)


def get_tree(request):
    """
    获取权限树e
    :param request:
    :return:
    """
    data = get_permissions()
    return write(data)


@csrf_exempt
def offline_active(request):
    state = True
    msg = '激活文件写入成功！'

    try:
        code = request.POST.get('code')
        utils.offline_active_code(code)
        request.reload = True

    except Exception as e:
        state = False
        msg = e.args[0]

    return write(None, msg, state)
