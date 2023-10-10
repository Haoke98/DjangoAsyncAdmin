from . import handlers as handlers

try:

    from django.utils.deprecation import MiddlewareMixin  
except ImportError:
    MiddlewareMixin = object  

import os


class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):

        val = os.environ.get('sp_is_ready')
        if not val:
            os.environ.setdefault('sp_is_ready', 'True')
            from . import urls
            urls.init()

        path = request.path
        if not path.endswith('/'):
            path = path + '/'

        return handlers.process_request(request, path)

    def process_view(self, request, view_func, view_args, view_kwargs):
        return handlers.process_view(request, view_func)

    def process_response(self, request, response):
        handlers.done(request)
        return response
