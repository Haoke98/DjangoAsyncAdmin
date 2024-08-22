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

