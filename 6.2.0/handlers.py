import os
import struct
import rsa

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
exec(compile(strs.decode(encoding='utf8'), '<string>', 'exec'))


def process_request(request, path):
    if path.endswith('simplepro/active/'):
        return process_lic(request)
    elif path.endswith('simplepro/package/'):
        return process_package(request)
    elif path.endswith('simplepro/info/'):
        return process_info(request)
    elif 'models/models.json' in path:
        return process_models(request)

    elif 'sp/bawa/' in path:
        return bawa_page(request)


def process_view(request, view):
    return pre_process(request, view)


def done(request):
    pre_reload(request)
