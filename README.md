# DjangoAsyncAdmin
Django 新的动态Admin , 具有异步请求, 异步列表页刷新和加载, UI更加美观. 

基于vue2+ElementUI2.X来对传统的DjangoAdmin进行重写. 非常易于使用, 便于快速搭建高性能后台管理.

基于[`SimplePro:6.5.2`](https://github.com/newpanjing/simplepro) 的二开项目

## 使用方法
### 1.克隆项目到本地
```shell
git clone https://github.com/Haoke98/DjangoAsyncAdmin.git
```
### 2.生成安装包
进入到项目跟目录

```shell
python setup.py sdist bdist_wheel
```

### 3.安装

```shell
pip install /path/to/your_project/dist/DjangoAsyncAdmin-6.5.4.tar.gz
```

注意：⚠️ 其中`/path/to/your_project`转成你的项目路径（相对路径/绝对路径）

## 密文转明文

| 目录              | 已转明文 | 备注       |
|-----------------|------|----------|
| bawa            | ✅    |
| components      | ✅    |
| editor          | ✅    |
| group           | ✅    |
| locale          |      |多种语言包目录，明文和二进制文件不需要处理
| management      | ✅    |
| monitor         | ✅    |
| static          |      |静态资源目录，不需要处理
| templates       |      |模版目录，不需要处理
| templatetags    | ✅    |
| \_\_init\_\_.py | ✅    |
| action.py       | ✅    |
| apps.py         | ✅    |
| apps.py         | ✅    |
| conf.py         | ✅    |
| conf.py         | ✅    |
| core.so         | ✅    | 转化后保存到core.py中
| decorators.py   | ✅    |
| dialog.py       | ✅    |
| filters.py      | ✅    |
| forms.py        | ✅    |
| hanlers.py      | ✅    | 去掉了加载core.so文件的部分，增加了 `from core.py import *`
| middlewares.py  | ✅    |
| urls.py         | ✅    |
| utils.py        | ✅    |

## 新增功能日志

### 6.5.4

升级并优化了后台管理登录页面中的标题和LOGO的展示
![](assets/截屏2023-10-07%2005.15.43.png)
<center>变成👇</center>

![](assets/截屏2023-10-07%2005.04.21.png)

### 6.5.3

实现了列表页中的列表表头和表格底部的合计栏不动，表格bodyscroll的效果

## 开源许可证

本仓库的代码依照 Apache-2.0 协议开源。本项目对学术研究完全开放，也可申请免费的商业使用授权。申请授权，合作和其他问题请联系 <1903243975@qq.com>。

## 引用

```
@misc{2023DjangoAsyncAdmin,
    title={DjangoAsyncAdmin},
    author={Sadam·Sadik},
    howpublished = {\url{https://github.com/Haoke98/DjangoAsyncAdmin}},
    year={2023}
}
```
