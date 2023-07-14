import base64
import json
import os
import struct

import requests
from django.core.management import BaseCommand

from simplepro import conf
from simplepro.utils import offline_active_code


class Command(BaseCommand):
    help = "Active simplepro"

    def add_arguments(self, parser):
        parser.add_argument('--code', action="store", nargs="+", default=[])

    def _offline_active(self, b64):
        try:
            offline_active_code(b64)
            print('激活成功')
        except Exception as e:
            print("激活失败：", e)

    def _print_and_scan(self):
        print('如果您没有激活码，请点击下方链接购买：\n'
              'https://simpleui.72wo.com/simplepro\n'
              , '-' * 50,
              "\n您的设备ID：{}\n".format(conf.get_device_id())
              , '-' * 50,
              '\n【请选择激活方式】\n'
              , '-' * 50,
              '\n1:在线激活\n2:离线激活\n3:退出')
        raw_input = input('请输入您的选择：')
        print('您选择了：%s' % raw_input)
        if raw_input == '1':
            code = input('请输入激活码：')

            device_id = conf.get_device_id()
            lic_file = os.path.join(os.getcwd(), 'simplepro.lic')
            url = conf.get_server_url() + '/active'
            r = requests.post(url, data={
                'device_id': device_id,
                'active_code': code
            })

            if r.status_code == 200:
                data = r.json()
                if data.get('state') is True:
                    
                    

                    f = open(lic_file, 'wb')

                    
                    d1 = base64.b64decode(data.get('license'))
                    d2 = base64.b64encode(bytes(data.get('private_key'), encoding='utf8'))

                    f.write(struct.pack('h', len(d1)))
                    f.write(struct.pack('h', len(d2)))

                    f.write(d1)
                    f.write(d2)

                    f.close()
                print(data.get('msg'))
            else:
                print("激活失败")
        elif raw_input == '2':
            b64 = input('激活文件内容：')
            self._offline_active(b64)
        elif raw_input == '3':
            print('退出激活')

    def handle(self, *args, **options):
        self._print_and_scan()
