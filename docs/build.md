# 打包及发布教程

## 1.生成安装包
进入到项目跟目录

```shell
python setup.py sdist bdist_wheel
```

## 2.安装

```shell
pip install /path/to/your_project/dist/DjangoAsyncAdmin-6.5.4.tar.gz
```

注意：⚠️ 其中`/path/to/your_project`转成你的项目路径（相对路径/绝对路径）

## 3.发布到PyPI


### 1. 安装PyPI的专用deploy工具

```shell
python3 -m pip install --upgrade twine
```
### 2. 注册账号
首先，你需要在TestPyPI上注册一个帐户，这是一个专门用于测试和实验的软件包索引实例。对于像本教程这样的情况，我们不一定希望将软件包上传到真实的索引中，TestPyPI非常适合。要注册一个帐户，请访问 https://test.pypi.org/account/register/ 并完成该页面上的步骤。在能够上传任何软件包之前，你还需要验证你的电子邮件地址。有关更多详细信息，请参阅使用TestPyPI。

### 3. 获取API令牌
为了安全地上传你的项目，你需要一个PyPI API令牌。在 https://test.pypi.org/manage/account/#api-tokens 上创建一个，将"Scope"设置为"Entire account"。在你复制和保存令牌之前，请不要关闭该页面——你将无法再次看到该令牌。
### 4. 配置~/.pypirc
```
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-<<<<<<<<--这是一个---API-TOKEN---可以从pypi.org网站上获取----example-->>>>>>>>>>>
```
### 4. Twine安装完成后，运行Twine以上传dist目录下的所有存档文件。
```shell
python3 -m twine upload --repository pypi dist/*
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