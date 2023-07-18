# SimpleProActivator 激活工具
An activator and anplanning analysis of the simplepro.
### 注意事项⚠️
生成的simplepro.lic授权文件, 必须放在simplepro被引用的WEB服务的运行时目录下

**⚠️重中之重⚠️**： 替换完simplepro.lic授权文件以后，已经启动的服务必须重启才会生效， 授权内容才会重新被读取并加载。

#### 问:怎么获取运行时目录?
在服务的代码中增加这样一样来, 让服务主动把路径输出到日志文件或者控制台中:
```python
import os
print("CWD:",os.getcwd())
```
