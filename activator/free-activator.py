# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/7/14
@Software: PyCharm
@disc:
======================================="""
import base64
import os
import struct
import uuid

import click
import requests
import rsa

from lib import rsaHelper

PrivateKeyBytes = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEqQIBAAKCAQEAjwp7crn495Qtvj47p3vq/sng488PsGioY0pHoapzAsNE5Kvf\nl0gnkS5nM8BqHGvsUXELEXgHS0J05SGCuBdJE13sCES4/zycYe33MV9NifRHvmes\nnalKZClnyx/r0bi5bRpgDZfCftZtIMoY99bJn7EfOwXO9kI2tSRzpJ3PY/5s4cbi\nd0IB5MYo9KLElIDNhQr4aZ/IsmE5jPGXVyMN0SABtb6nNJDYr9nakuHwNHfFOXBM\nJE0IXsMzMFSOsPPlaD/Zev1FFgxMCXebfVYE2U9gsM2LeuUCM0OampeG9gMV2j9F\ngw7/j5OTL4+d/jLaMrUcCGAWLF9IbG1AhCs2LwIDAQABAoIBACLNwB+4FFXZHhAu\nAEHOKu13nVqQpRadQGt4RVmWqYlAjeC92RdsHQR8L+wtoyPrNoLSaIkFlXDAaMTf\nlHjKYaNutOGGJyUjUEGbrwu6TpmEcHhprVxnNoyMbo7D45MRyTw8sKZeCJrn/YF+\n6vhSsJhEdn7b+PF+RrJB8oViqONsQ9NqL/Ag9s/4FSeHQY15uKHeA+ScQbpGnvqQ\nt44llJoWCzfFX/2R0JOtGzAIXyg8NeXE73MX/eHyXTdwOQXCFNmtf0mwiJJogTww\n98EJo1fTnKxjkQ1xzoevkh4QZI4grISlGNyQxSuMP4E3oPo/znY6XtmameAW6C+S\nWZ8pWKECgYkA0jjkaxdmbVGhUe5jaHD/uYkiccz0Lseqy4SnC7s8VLou3pY+xaUV\nUqRqlHTaqIXBK+qI0PHv8i7kAF/I2ulrXmebDf0ppPUn37xzdHwAfJ+lTnwd1C4Q\ndLBz0YHds56jCj5Bf+tl6x94U1Y/DWP+Bi7BzHesC52/qD9xv9CiFc1Zja7FYPCl\nWQJ5AK4we6LnqgeCq83Tt3kDD9kswtjKmnbUombT0Vxs+jXTY7w4mTL1v+9T0WfD\niPj/clapu5JOYO+jwQzvbh8bxkM0goAho1quBSW1SutEMJvP/0dFCtWzECKaAYnM\nu/WIpMJt0989FUdsED3oYaVT31TDIX0fDwRexwKBiDbXgrdxZlY0ino+T46qk/wK\nC4NWrYkaq7LmS1HjKa0M2TdWSM/07igeHnPWPEjkg+16BPFFfIxYsUBrvJFnfYwm\nSSwQFHIlRp62ogQMaXAZkd10wa9dyQs4ES7hyz2VsAD3Fs1RUshQ8GoFQPO0V0uz\nnPlDaw2ovJwe2QTqX66CYM92faV5ghkCeFU7nAPGX8h1BCQe6LPp76NQ57a0zIhA\n24Z9NwCGwpf76915xFzPKy+sT9b6MtfEBuqo+wNIHt6jvh7aOYQ3TvgrhX+09f21\nEQe2ggZEw5Q6Xqs8+WQ/zjFgMkh/SamHRzdsDjQ562ObWQcx4jXHqIwNPyG+RNba\nmQKBiQCzU2rerza3PiZUY1QyeVoC/M/yUKGuw7LHrjAOd30E8SQws7COjl7spQiX\neP4Ptk+rowUZpeWoWxxOAeDQbcCw99Zpxjspakz33F6+7kJPpeL/w4VsnwcIpK5E\nPlOj0uXBFn73Xy9C3bLmeA/alvpC/DFYHLCVp79c8T1790vg6kcrSzvwbC+w\n-----END RSA PRIVATE KEY-----\n'


def get_server_url():
    return 'https://simpleui.72wo.com'


def _get_serial_number():
    array = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
             '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
             '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53',
             '54', '55', '56', '57', '58', '59', '60', '61']
    uid = str(uuid.uuid4()).replace("-", '')

    buffer = []
    for i in range(0, 8):
        start = i * 4
        end = i * 4 + 4
        val = int(uid[start:end], 16)
        buffer.append(array[val % 62])
    return "".join(buffer)


def get_device_id():
    p = os.path.join(os.path.expanduser('~'), '.sn')
    if os.path.exists(p):
        with open(p, 'r') as f:
            sn = f.read()
    else:
        sn = _get_serial_number()
        with open(p, 'w') as f:
            f.write(sn)
    print(p, sn)
    return sn


def online_active_code(code):
    """
    在线激活模式
    {'state': True, 'msg': '激活成功', 'license': 'Vv+ICkz5vKoZImXGIXtR7k5rP/XduVlPjqQ9fsJvZZ2BC2u8+WJbNkwnP2AX6/neTCLRmIb/uC+zSS2jskdJYhqAYveZf2IHkhqNirCSGJLuHyxuRkLxK8UbvcL4xYykqWifGRmxknS3WItSq6RdCLkqm37zYwKSdqGzMaoukn64se9H47udTyFO7FiGd6BLoolr/nDCQdk9YCeyyJQh62oSYEGRBVEahc1rUl4moFcudnjWieFAl9e1D6bJF7L1nV/KYdCdyqv+biHh6c7Oy9bVqiWLAL7jCjzQRWaGEdjZmAiavLajdcxJcl+e8NW3UbSEWOI5ia0RXxqSL4wE8Q==', 'private_key': '-----BEGIN RSA PRIVATE KEY-----\nMIIEqQIBAAKCAQEAjwp7crn495Qtvj47p3vq/sng488PsGioY0pHoapzAsNE5Kvf\nl0gnkS5nM8BqHGvsUXELEXgHS0J05SGCuBdJE13sCES4/zycYe33MV9NifRHvmes\nnalKZClnyx/r0bi5bRpgDZfCftZtIMoY99bJn7EfOwXO9kI2tSRzpJ3PY/5s4cbi\nd0IB5MYo9KLElIDNhQr4aZ/IsmE5jPGXVyMN0SABtb6nNJDYr9nakuHwNHfFOXBM\nJE0IXsMzMFSOsPPlaD/Zev1FFgxMCXebfVYE2U9gsM2LeuUCM0OampeG9gMV2j9F\ngw7/j5OTL4+d/jLaMrUcCGAWLF9IbG1AhCs2LwIDAQABAoIBACLNwB+4FFXZHhAu\nAEHOKu13nVqQpRadQGt4RVmWqYlAjeC92RdsHQR8L+wtoyPrNoLSaIkFlXDAaMTf\nlHjKYaNutOGGJyUjUEGbrwu6TpmEcHhprVxnNoyMbo7D45MRyTw8sKZeCJrn/YF+\n6vhSsJhEdn7b+PF+RrJB8oViqONsQ9NqL/Ag9s/4FSeHQY15uKHeA+ScQbpGnvqQ\nt44llJoWCzfFX/2R0JOtGzAIXyg8NeXE73MX/eHyXTdwOQXCFNmtf0mwiJJogTww\n98EJo1fTnKxjkQ1xzoevkh4QZI4grISlGNyQxSuMP4E3oPo/znY6XtmameAW6C+S\nWZ8pWKECgYkA0jjkaxdmbVGhUe5jaHD/uYkiccz0Lseqy4SnC7s8VLou3pY+xaUV\nUqRqlHTaqIXBK+qI0PHv8i7kAF/I2ulrXmebDf0ppPUn37xzdHwAfJ+lTnwd1C4Q\ndLBz0YHds56jCj5Bf+tl6x94U1Y/DWP+Bi7BzHesC52/qD9xv9CiFc1Zja7FYPCl\nWQJ5AK4we6LnqgeCq83Tt3kDD9kswtjKmnbUombT0Vxs+jXTY7w4mTL1v+9T0WfD\niPj/clapu5JOYO+jwQzvbh8bxkM0goAho1quBSW1SutEMJvP/0dFCtWzECKaAYnM\nu/WIpMJt0989FUdsED3oYaVT31TDIX0fDwRexwKBiDbXgrdxZlY0ino+T46qk/wK\nC4NWrYkaq7LmS1HjKa0M2TdWSM/07igeHnPWPEjkg+16BPFFfIxYsUBrvJFnfYwm\nSSwQFHIlRp62ogQMaXAZkd10wa9dyQs4ES7hyz2VsAD3Fs1RUshQ8GoFQPO0V0uz\nnPlDaw2ovJwe2QTqX66CYM92faV5ghkCeFU7nAPGX8h1BCQe6LPp76NQ57a0zIhA\n24Z9NwCGwpf76915xFzPKy+sT9b6MtfEBuqo+wNIHt6jvh7aOYQ3TvgrhX+09f21\nEQe2ggZEw5Q6Xqs8+WQ/zjFgMkh/SamHRzdsDjQ562ObWQcx4jXHqIwNPyG+RNba\nmQKBiQCzU2rerza3PiZUY1QyeVoC/M/yUKGuw7LHrjAOd30E8SQws7COjl7spQiX\neP4Ptk+rowUZpeWoWxxOAeDQbcCw99Zpxjspakz33F6+7kJPpeL/w4VsnwcIpK5E\nPlOj0uXBFn73Xy9C3bLmeA/alvpC/DFYHLCVp79c8T1790vg6kcrSzvwbC+w\n-----END RSA PRIVATE KEY-----\n', 'rid': 2524}
    """
    device_id = get_device_id()

    url = get_server_url() + '/active'
    r = requests.post(url, data={
        'device_id': device_id,
        'active_code': code
    })

    if r.status_code == 200:
        data = r.json()
        print(data)
        if data.get('state') is True:
            # 获取根目录，写入激活文件
            # 内容需要混淆写入

            f = open('simplepro.lic', 'wb')

            # d1 = bytes(data.get('license'), encoding='utf8')
            d1 = base64.b64decode(data.get('license'))
            d2 = base64.b64encode(bytes(data.get('private_key'), encoding='utf8'))

            f.write(struct.pack('h', len(d1)))
            f.write(struct.pack('h', len(d2)))

            f.write(d1)
            f.write(d2)

            f.close()


@click.command()
@click.option("-c", "--code", help="激活码")
@click.option("-i", "--device-id", help="设备ID")
@click.option("-d", "--end-date", help="授权截止日期")
def generate_lic_file(code, device_id, end_date):
    """
        生成授权文件simplepro.lic
    """
    if device_id is None:
        device_id = get_device_id()
    # 获取根目录，写入激活文件
    # 内容需要混淆写入
    origStr = '''{"end_date": "%s", "code": "%s", "device_id": "%s"}''' % (end_date, code, device_id)
    print(origStr)
    pub_key = rsaHelper.generate_public_key(PrivateKeyBytes)
    crypto = rsa.encrypt(origStr.encode('ascii'), pub_key)
    # 解密字符串
    # priv_key = rsa.PrivateKey.load_pkcs1(PrivateKeyBytes)
    # decrypted = rsa.decrypt(crypto, priv_key).decode()
    # print(decrypted)
    d1 = crypto
    # print("d1", d1)
    d2 = base64.b64encode(PrivateKeyBytes)
    with open("simplepro.lic", 'wb') as f:
        print(len(d1), len(d2))
        f.write(struct.pack('h', len(d1)))
        f.write(struct.pack('h', len(d2)))
        f.write(d1)
        f.write(d2)


if __name__ == '__main__':
    generate_lic_file()
