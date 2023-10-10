import base64
import os
import datetime
import json

from django.views import generic
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from . import utils
from .widgets import MDConfig

MDEDITOR_CONFIGS = MDConfig('default')

UEDITOR_SERVER_CONFIG = {"imageActionName": "uploadimage", "imageFieldName": "upfile", "imageMaxSize": "2048000",
                         "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], "imageCompressEnable": "true",
                         "imageCompressBorder": "1600", "imageInsertAlign": "none", "imageUrlPrefix": "",

                         "scrawlActionName": "uploadscrawl", "scrawlFieldName": "upfile",
                         "scrawlPathFormat": "/ueditor/upload/image/{yyyy}{mm}{dd}/{time}{rand:6}",
                         "scrawlMaxSize": "2048000", "scrawlUrlPrefix": "", "scrawlInsertAlign": "none",
                         "snapscreenActionName": "uploadimage",

                         "snapscreenUrlPrefix": "", "snapscreenInsertAlign": "none",
                         "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"],
                         "catcherActionName": "catchimage",
                         "catcherFieldName": "source",

                         "catcherUrlPrefix": "", "catcherMaxSize": "2048000",
                         "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
                         "videoActionName": "uploadvideo",
                         "videoFieldName": "upfile",

                         "videoMaxSize": "102400000",
                         "videoAllowFiles": [".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg", ".ogg",
                                             ".ogv",
                                             ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"],
                         "fileActionName": "uploadfile", "fileFieldName": "upfile",

                         "fileMaxSize": "51200000",
                         "fileAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".flv", ".swf", ".mkv", ".avi",
                                            ".rm",
                                            ".rmvb", ".mpeg", ".mpg", ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm",
                                            ".mp3",
                                            ".wav", ".mid", ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab",
                                            ".iso",
                                            ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md",
                                            ".xml"],
                         "imageManagerActionName": "listimage",

                         "imageManagerListSize": "20", "imageManagerUrlPrefix": "", "imageManagerInsertAlign": "none",
                         "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
                         "fileManagerActionName": "listfile",

                         "fileManagerUrlPrefix": "", "fileManagerListSize": "20",
                         "fileManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".flv", ".swf", ".mkv",
                                                   ".avi",
                                                   ".rm", ".rmvb", ".mpeg", ".mpg", ".ogg", ".ogv", ".mov", ".wmv",
                                                   ".mp4",
                                                   ".webm", ".mp3", ".wav", ".mid", ".rar", ".zip", ".tar", ".gz",
                                                   ".7z",
                                                   ".bz2", ".cab", ".iso", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
                                                   ".pptx",
                                                   ".pdf", ".txt", ".md", ".xml"]}


class UploadScrawl:

    def __init__(self, upfile):
        self.data = base64.b64decode(upfile)

    @property
    def _name(self):
        return 'uploadscrawl.png'

    def read(self):
        return self.data


def upload(request, action=None):
    if action == 'scrawl':
        upload_image = UploadScrawl(upfile=request.POST.get('upfile'))
    else:
        for file in request.FILES:
            upload_image = request.FILES.get(file)
            break

    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL

    suffix = os.path.splitext(upload_image._name)[1]
    target_name = utils.get_short_uuid() + suffix

    if not os.path.exists(media_root):
        os.mkdir(media_root)

    file_path = os.path.join(media_root, target_name)
    with open(file_path, 'wb') as w:
        w.write(upload_image.read())

    url = "{}/{}".format(media_url, target_name)

    results = {
        "name": target_name,
        "original": upload_image._name,
        "size": "",
        "state": "SUCCESS",
        "type": "png",
        "url": url
    }

    return HttpResponse(json.dumps(results))


def handler(request):
    setattr(request, '_dont_enforce_csrf_checks', True)
    action = request.GET.get("action", "")

    if action == 'uploadscrawl':
        return upload(request, action='scrawl')
    else:
        return upload(request)


class UploadView(generic.View):
    """ upload image file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get('action') == 'config':
            return HttpResponse(json.dumps(UEDITOR_SERVER_CONFIG), content_type='application/json')

    def post(self, request, *args, **kwargs):

        if request.GET.get('action'):
            return handler(request)

        for file in request.FILES:
            upload_image = request.FILES.get(file)
            break

        media_root = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL

        if not upload_image:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            }))

        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)
        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
            return HttpResponse(json.dumps({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    MDEDITOR_CONFIGS['upload_image_formats']),
                'url': ""
            }))

        suffix = os.path.splitext(upload_image._name)[1]
        target_name = utils.get_short_uuid() + suffix

        if not os.path.exists(media_root):
            os.mkdir(media_root)

        file_path = os.path.join(media_root, target_name)
        with open(file_path, 'wb') as w:
            w.write(upload_image.read())

        url = "{}{}".format(media_url, target_name)
        return HttpResponse(json.dumps({'success': 1,
                                        'message': "上传成功！",
                                        'url': url}))
