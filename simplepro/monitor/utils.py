import psutil


def get_monitor():
    """ 定义函数 实时获取硬件信息 """

    cup_per = psutil.cpu_percent(1)

    memory_info = psutil.virtual_memory()

    net_info = psutil.net_io_counters()

    return {
        'cpu': {
            'count': psutil.cpu_count(logical=False),
            'used': cup_per
        },
        'memory': {
            'total': memory_info.total / 1024 / 1024 / 1024,
            'used': memory_info.percent
        },

        'net': {
            'recv': net_info.bytes_recv / 1024,
            'sent': net_info.bytes_sent / 1024,

        }
    }


if __name__ == '__main__':
    print(get_monitor())
