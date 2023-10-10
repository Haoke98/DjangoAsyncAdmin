from simplepro.core import *


def process_request(request, path):
    if path.endswith('simplepro/active/'):
        return process_lic(request)
    elif path.endswith('simplepro/package/'):
        return process_package(request)
    elif path.endswith('simplepro/info/'):
        return process_info(request)
    elif 'models/models.json' in path:
        return process_models(request)

    elif 'sp/bawa/' in path:
        return bawa_page(request)


def process_view(request, view):
    return pre_process(request, view)


def done(request):
    pre_reload(request)
