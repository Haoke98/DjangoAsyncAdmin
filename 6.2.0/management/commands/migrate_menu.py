from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

try:
    from django.utils.translation import ugettext as _
except:
    from django.utils.translation import gettext as _


def save_item(item):
    name = item.get('name')
    codename = item.get('codename')
    ct, exists = ContentType.objects.get_or_create(
        app_label=name,
        model=codename,
    )

    
    permission = Permission.objects.filter(codename=codename, content_type=ct)
    if not permission.exists():
        Permission.objects.create(
            name=name,
            codename=codename,
            content_type=ct,
        )
        print('create permission: {}'.format(item))


def save(data):
    print(_("Synchronization menu"), "Condition：codename!=null")
    print(data)
    
    
    
    for item in data:
        save_item(item)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if hasattr(settings, 'SIMPLEUI_CONFIG') and "menus" in settings.SIMPLEUI_CONFIG:
            config = settings.SIMPLEUI_CONFIG
            r = self.handler_menus(config.get('menus'))
            save(r)
        else:
            print(_("Configure SIMPLEUI_CONFIG in settings.py"))
            print("https://simpleui.72wo.com/docs/simplepro/config.html

    def handler_menus(self, menus):
        arrays = []
        for menu in menus:
            if 'codename' in menu and 'name' in menu:
                arrays.append({
                    'name': menu.get('name'),
                    'codename': menu.get('codename'),
                })
                if 'models' in menu:
                    arrays.extend(self.handler_menus(menu.get('models')))
        return arrays
