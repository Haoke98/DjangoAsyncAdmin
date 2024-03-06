# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/10/10
@Software: PyCharm
@disc:
======================================="""
from setuptools import setup, find_packages

requires = ['django>=2.1', 'django-simpleui>=2022.11.30', 'django-import-export', 'requests', 'rsa', 'psutil>=5.9.8']
setup(packages=find_packages(exclude=[]), install_requires=requires)
