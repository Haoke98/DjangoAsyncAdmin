# SimpleProActivator 激活工具

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
