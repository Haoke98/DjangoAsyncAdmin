# SimplePro+

## 1. SimplePro二开版本

### 新增功能日志
#### 6.5.3
实现了列表页中的列表表头和表格底部的合计栏不动，表格bodyscroll的效果
#### 6.5.4
升级并优化了后台管理登录页面中的标题和LOGO的展示
![](assets/截屏2023-10-07%2005.15.43.png)

<center></center>
<center>变成👇</center>


![](assets/截屏2023-10-07%2005.04.21.png)
## 2. SimpleProActivator 激活工具

`目前仅仅是支持版本<=6.5.2`
### 使用方法
```shell
python free-activator.py -c uIDVzdy9 -i 4154104401335502 -d "3023-07-18 16:26:56"
```
只需替换其中设备ID:`4154104401335502`
### 注意事项⚠️

生成的simplepro.lic授权文件, 必须放在simplepro被引用的WEB服务的运行时目录下

**⚠️重中之重⚠️**： 替换完simplepro.lic授权文件以后，已经启动的服务必须重启才会生效， 授权内容才会重新被读取并加载。

#### 问:怎么获取运行时目录?

在服务的代码中增加这样一样来, 让服务主动把路径输出到日志文件或者控制台中:

```python
import os
print("CWD:",os.getcwd())
```
