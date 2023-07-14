import os

import psutil


def get_rate(func):
    import time

    key_info, old_recv, old_sent = func()  

    time.sleep(1)

    key_info, now_recv, now_sent = func()  

    net_in = {}
    net_out = {}

    for key in key_info:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024)  

    return key_info, net_in, net_out


def get_key():
    key_info = psutil.net_io_counters(pernic=True).keys()  

    recv = {}
    sent = {}

    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)  
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)  

    return key_info, recv, sent











gb = 1024 * 1024 * 1024
def get_memory():
    r = psutil.virtual_memory()
    total = r.total / gb
    used = r.used / gb
    return total, used


def get_disk():
    partition = psutil.disk_usage('/')
    print(partition)

    return partition.total / gb, partition.used / gb


def get_self_used():
    return psutil.Process(os.getpid()).memory_info().rss/1024/1024


if __name__ == '__main__':
    print(get_memory())
    
    
