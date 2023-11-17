#!/bin/bash
##conda create --name django_async_admin --clone simplepro
##conda deactivate
#conda remove --name simplepro --all
rm -rf dist/*
python setup.py sdist bdist_wheel
/Users/shadikesadamu/anaconda3/envs/allkeeper/bin/pip install dist/DjangoAsyncAdmin-*.tar.gz