# 组件文档

继承于 [SimplePro组件文档](https://www.mldoo.com/docs/simplepro/widget/checkbox.html#%E5%A4%8D%E9%80%89%E6%A1%86%E7%BB%84%E4%BB%B6)

## 基础组件

## 表单组件

### 密码组件

继承自`froms.CharField`表单字段

#### 效果

![](static/截屏2023-11-15%2016.20.58.png)

#### 如何引入

```python
from simplepro.components.forms import PasswordFormField
```

#### 参数

| 参数名          | 类型  | 必须  | 默认值                                                                      | 说明         |
|--------------|-----|-----|--------------------------------------------------------------------------|------------|
| label        | 字符串 | ☑️  |                                                                          | 表单中的字段展示名称 |
| required     | 布尔值 | ☑️  | False                                                                    | 是否必填       |
| encryptByMd5 | 布尔值 | ☑️  | True                                                                     | 是否要MD5加密   |
| lenMin       | 数字  | ☑️  | 6                                                                        | 最小长度       |
| lenMax       | 数字  | ☑️  | 48                                                                       | 最大长度       |
| pattern      | 字符串 | ☑️  | "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-$%&@+!" | 随机生成的可选字符集 |

其他参数都继承`forms.CharField`.

#### 示例

```python
from django.forms import ModelForm
from simplepro.components.forms import PasswordFormField

from .models import DbServiceUser


class DbServiceUserForm(ModelForm):
    password = PasswordFormField(label="密码", required=False, encryptByMd5=False)

    class Meta:
        model = DbServiceUser
        fields = ['owner', 'service', 'username', 'password', 'hasRootPriority']

```