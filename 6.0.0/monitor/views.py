from django.views.generic import View

from simplepro.monitor import utils
from django.http import JsonResponse


class MonitorView(View):
    """
    获取数据：

    入网带宽、出网带宽
    CPU使用率
    内存使用率
    磁盘使用率
    
    """

    def post(self, request):
        return JsonResponse(data=utils.get_monitor())
