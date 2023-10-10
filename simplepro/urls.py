from django.urls import path
from .group import view
from .bawa import views as bawa_views
from simplepro.editor import views as editor_views
from .monitor.views import MonitorView

app_name = 'sp'

urlpatterns = [
    path('group/action/', view.action, name='action'),
    path('offline/active/', view.offline_active, name='offline_active'),
    path('editor/upload', editor_views.UploadView.as_view(), name='editor_upload'),
    path('bawa/', bawa_views.page, name='bawa_page'),
    path('bawa/save', bawa_views.save, name='bawa_save'),
    path('bawa/data', bawa_views.get_data, name='bawa_data'),
    path('monitor/data', MonitorView.as_view(), name='monitor')
]


def init():
    from django.conf import settings
    from django.urls import include
    from simplepro import urls as sp_urls

    urls = __import__(settings.ROOT_URLCONF).urls

    urls.urlpatterns.append(
        path(r'^{}/'.format(sp_urls.app_name), include('simplepro.urls', namespace=sp_urls.app_name))
    )









