import json
import os

from django.http import HttpResponse
from django.shortcuts import render

try:
    from django.utils.translation import ugettext as _
except:
    from django.utils.translation import gettext as _
from django.conf import settings
save_dir = os.path.join(settings.BASE_DIR, 'bawa')
save_file = os.path.join(save_dir, 'bawa_data.json')


def page(request):
    response = render(request, 'admin/bawa/render.html')
    return response


def save(request):
    rs = {
        'msg': _('Successfully'),
        'success': True
    }

    try:

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        r = request.POST.get('data')
        bawa_data = json.loads(r)
        with open(save_file, 'w') as f:
            json.dump(bawa_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        rs = {
            'msg': _('Server error') + e,
            'success': False
        }
    return HttpResponse(json.dumps(rs), content_type='application/json')


def get_data(request):
    str_data = '[]'
    if os.path.exists(save_file):
        with open(save_file, 'rb') as f:
            str_data = f.read()

    return HttpResponse(str_data, content_type='application/json')
