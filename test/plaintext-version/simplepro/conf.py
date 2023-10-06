import os
import uuid


def get_server_url():
    return 'https://simpleui.72wo.com'


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


if __name__ == '__main__':
    print(_get_serial_number())
    print(get_device_id())
# 0013212354224823
# 2426506130533021
