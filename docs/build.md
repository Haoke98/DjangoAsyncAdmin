# 打包及发布教程

##### 1.生成安装包
进入到项目跟目录

```shell
python setup.py sdist bdist_wheel
```

#### 2.安装

```shell
pip install /path/to/your_project/dist/DjangoAsyncAdmin-6.5.4.tar.gz
```

注意：⚠️ 其中`/path/to/your_project`转成你的项目路径（相对路径/绝对路径）

#### 3.发布到PyPI (Uploading the distribution archives)

1. 安装PyPI的专用deploy工具

```shell
python3 -m pip install --upgrade twine
```
2. Twine安装完成后，运行Twine以上传dist目录下的所有存档文件。
```shell
python3 -m twine upload --repository testpypi dist/*
```
你将被要求输入用户名和密码。对于用户名，请使用__token__。对于密码，请使用令牌值，包括 pypi- 前缀。

命令完成后，你应该会看到类似于以下内容的输出：
```shell
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: __token__
Uploading example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.2/8.2 kB • 00:01 • ?
Uploading example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.8/6.8 kB • 00:00 • ?
```