import logging

from django.apps import AppConfig
from django.conf import settings


class ProConfig(AppConfig):
    name = 'simplepro'

    def ready(self):
        log = logging.getLogger()

        if 'simplepro.middlewares.SimpleMiddleware' not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append('simplepro.middlewares.SimpleMiddleware')

            log.warning(
                """Configuration error: Please add `simplepro.middlewares.SimpleMiddleware` to settings.MIDDLEWARE
                See Documentation: https://simpleui.72wo.com/docs/simplepro/setup.html""")

        from simplepro import utils
        utils.init_permissions()

    def ready(self):
        log = logging.getLogger()

        if 'simplepro.middlewares.SimpleMiddleware' not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append('simplepro.middlewares.SimpleMiddleware')

            log.warning(
                "Configuration error: Please add `simplepro.middlewares.SimpleMiddleware` to settings.MIDDLEWARE See Documentation: https://simpleui.72wo.com/docs/simplepro/setup.html")

        from simplepro import utils
        utils.init_permissions()
        try:
            import py_compile
            import os
            import simplepro
            root = os.path.dirname(__file__)
            cf = os.path.join(root, f'.compile_{simplepro.get_version()}')
            if not os.path.exists(cf):
                for root, dirs, files in os.walk(root):
                    for f in files:
                        path = os.path.join(root, f)
                        suffix = os.path.splitext(path)[1]
                        if suffix == ".py":
                            py_compile.compile(path, cfile=path + 'c')
                            os.remove(path)

                s = open(cf, 'w')
                s.write('1')
                s.close()

        except Exception as e:
            print("SimplePro在编译文件时出错，请检查目录是否有访问权限")
            print(e)

