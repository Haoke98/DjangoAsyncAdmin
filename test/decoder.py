# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/7/14
@Software: PyCharm
@disc:
======================================="""
import base64
import lzma
import re

EXCLUDES = ['./decoder.py']
if __name__ == '__main__':
    import os

    # Specify the directory to traverse
    root_dir = '6.5.2'
    # Traverse the directory recursively
    for root, dirs, fns in os.walk(root_dir):
        for fn in fns:
            # Check if file ends with .py
            if fn.endswith('.py'):
                fp = os.path.join(root, fn)
                if fp not in EXCLUDES:
                    with open(fp, 'r', encoding='utf-8') as f:
                        txt = f.read()
                        match = re.search(r"b'(.*?)'", txt)
                        print(fp, end='   ')
                        if match:
                            b = match.group(1)
                            resp = lzma.decompress(base64.b64decode(b))
                            print(resp)
                            with open(fp, 'wb') as ff:
                                ff.write(resp)
                        else:
                            print("（该文件没有加密内容）")
