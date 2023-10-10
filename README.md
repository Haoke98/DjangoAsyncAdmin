# SimplePlus+
基于`SimplePro:6.5.2`二开项目
## 使用方法
### 1.克隆项目到本地
```shell
git clone https://github.com/Haoke98/SimplePlus.git
```
### 2.生成安装包
进入到项目跟目录

```shell
python setup.py sdist 
```

### 3.安装

```shell
pip install /path/to/your_project/dist/simplePlus-6.5.4.tar.gz
```

注意：⚠️ 其中`/path/to/your_project`转成你的项目路径（相对路径/绝对路径）

## 密文转明文

| 目录              | 已转明文 | 备注       |
|-----------------|------|----------|
| bawa            | ❌    |
| components      | ✅    |
| editor          | ✅    |
| ·········       | ❌    |
| static          |      |静态资源目录，不需要处理
| templates       |      |模版目录，不需要处理
| templatetags    | ❌    |
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
| hanlers.py      | ✅    | 内容已经少做修改，去掉了加载core.so文件的部分，增加了from core.py import *
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