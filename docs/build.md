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
#### 3.发布
```shell
twain 
```