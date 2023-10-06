# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/7/14
@Software: PyCharm
@disc:
======================================="""
import base64
import json
import os
import struct

import rsa


def core_so2py():
    so_file = open(os.path.join(os.path.dirname(__file__), '.core.so'), 'rb')
    buffer = so_file.read(2)
    r, = struct.unpack('h', buffer)
    buffer = so_file.read(r)
    pri = buffer
    strs = bytearray()
    while True:
        temp = so_file.read(4)
        if len(temp) == 0:
            so_file.close()
            break
        size, = struct.unpack('i', temp)
        d = so_file.read(size)
        privkey = rsa.PrivateKey.load_pkcs1(pri)
        strs.extend(rsa.decrypt(d, privkey))
    print(strs)
    with open("core.py", 'wb') as f:
        f.write(strs)


def read_lic_file(fp):
    f = open(fp, 'rb')
    buffer = f.read()
    a, = struct.unpack('h', buffer[0:2])
    b, = struct.unpack('h', buffer[2:4])
    print("a:", a, "b:", b)
    d1 = buffer[4:a + 4]
    d2 = base64.b64decode(buffer[a + 4:a + 4 + b])

    # 文件被改动移动过

    # decode
    pk = rsa.PrivateKey.load_pkcs1(d2)
    print(buffer[a + 4:a + 4 + b])
    print("-" * 50)
    print(d2)
    print("-" * 50)
    print(pk)
    print("-" * 50)
    print("d1", d1)
    print("-" * 50)
    text = rsa.decrypt(d1, pk).decode()  # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str
    print(text)


if __name__ == '__main__':
    # read_lic_file('../simplepro.lic')
    read_lic_file('/Users/shadikesadamu/Projects/izbasar/django-admin/simplepro.lic')
    read_lic_file('./simplepro.lic')
