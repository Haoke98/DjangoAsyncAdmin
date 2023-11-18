# DjangoAsyncAdmin

DjangoAsyncAdmin is a new dynamic admin interface for Django, featuring asynchronous requests, asynchronous page updates and loading, and a more attractive UI. It is based on vue2+ElementUI2.X and is a simple and efficient solution for high-performance backend management.

This project is based on [`SimplePro:6.5.2`](https://github.com/newpanjing/simplepro) and is open-source, with no licensing or activation required.

[![](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Haoke98/DjangoAsyncAdmin)
[![Gitee](https://img.shields.io/badge/Gitee-C71D23?style=for-the-badge&logo=gitee&logoColor=white)](https://gitee.com/sadam98/DjangoAsyncAdmin)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![](https://img.shields.io/badge/Google_chrome-4285F4?style=for-the-badge&logo=Google-chrome&logoColor=white)

![](https://img.shields.io/github/followers/Haoke98.svg?style=social&label=Follow&maxAge=2592000)
![](https://img.shields.io/github/license/Haoke98/DjangoAsyncAdmin.svg)
![](https://img.shields.io/github/downloads/Haoke98/DjangoAsyncAdmin/total.svg)
![](https://img.shields.io/github/forks/Haoke98/DjangoAsyncAdmin.svg)
![](https://img.shields.io/github/stars/Haoke98/DjangoAsyncAdmin.svg)
![](https://img.shields.io/github/watchers/Haoke98/DjangoAsyncAdmin.svg)
![GitHub language count](https://img.shields.io/github/languages/count/Haoke98/DjangoAsyncAdmin)
![GitHub search hit counter](https://img.shields.io/github/search/Haoke98/DjangoAsyncAdmin/django)
![GitHub top language](https://img.shields.io/github/languages/top/Haoke98/DjangoAsyncAdmin)
![GitHub contributors](https://img.shields.io/github/contributors/Haoke98/DjangoAsyncAdmin)

![](http://ForTheBadge.com/images/badges/made-with-python.svg)
[![forthebadge](https://haoke98.github.io/DjangoAsyncAdmin/static/MADE%20WITH-JetBrains-PyCharm.svg)](https://forthebadge.com)

## Inspiration
* thinkPHP
* simpleUI
* simplePro

## Demo
* [Digital World](https://github.com/Haoke98/AllKeeper)
![](https://haoke98.github.io/DjangoAsyncAdmin/static/digital_world_banner.png)
* [AI Lab](#)
![](https://haoke98.github.io/DjangoAsyncAdmin/static/silk_road_ai_banner.png)

## Features
<table>
<tr><td>Feature</td><td>Sub-Feature</td><td>Sub-Sub-Feature</td><td>Status</td></tr>
<tr><td>Optimized List Pages</td><td>Separated Front-End and Back-End Loading of Data</td><td>·········</td><td>✅</td></tr>
<tr><td>Visualized Homepage Design</td><td>·········</td><td>·········</td><td>✅</td></tr>
<tr><td>Multiple Customizable Theme Skins</td><td>·········</td><td>·········</td><td>✅</td></tr>
<tr><td rowspan="8">Rich Component Library</td><td>Integration of Almost All Element-UI Components</td><td>·········</td><td>✅</td></tr>
<tr><td rowspan="3">Diverse Kinds of Editors</td><td>Rich Text Editor</td><td>✅</td></tr>
<tr><td>Markdown Editor</td><td>✅</td></tr>
<tr><td>Json Editor</td><td>✅</td></tr>
<tr>
<td rowspan="2">Media Components</td>
<td>Image Upload Component</td><td>✅</td>
</tr>
<tr><td>Video Playback Component</td><td>✅</td></tr>
<tr><td rowspan="2">Advanced Components</td><td>Map Component</td><td>✅</td></tr>
<tr><td>Password Input Component</td><td>✅</td></tr>
<tr><td rowspan="4">Supports Customization</td><td>Custom Buttons</td><td>·········</td><td>✅</td></tr>
<tr><td>Custom Menus</td><td>·········</td><td>✅</td></tr>
<tr><td>Custom Permissions</td><td>·········</td><td>✅</td></tr>
<tr><td>Custom Dialog Boxes</td><td>·········</td><td>✅</td></tr>
<tr><td>·········</td><td>·········</td><td>·········</td><td>✅</td></tr>
<tr><td>Optimized Permissions</td><td>·········</td><td>·········</td><td>✅</td></tr>
</table>

## Usage
### Basics
* Component Documentation [DjangoAsyncAdmin Components Docs](https://haoke98.github.io/DjangoAsyncAdmin/components.html)
* Packaging and Deployment Documentation [Package And Deploy](https://haoke98.github.io/DjangoAsyncAdmin/build.html)
* Installation and Configuration [Temporary Reference](https://www.mldoo.com/docs/simplepro/guide/project_config.html)
### Advanced Configuration
* Global Configuration [Temporary Reference](https://www.mldoo.com/docs/simplepro/config/global/)
* Admin Configuration [Temporary Reference](https://www.mldoo.com/docs/simplepro/config/admin/field.html)
* Theme Configuration [Temporary Reference](https://www.mldoo.com/docs/simplepro/config/theme.html)
* JS-SDK [Temporary Reference](https://www.mldoo.com/docs/simplepro/config/jssdk.html)
* Custom Permissions [Temporary Reference](https://www.mldoo.com/docs/simplepro/config/permissions.html)
* Visualization Icons [Temporary Reference](https://www.mldoo.com/docs/simplepro/config/chat.html)
* Rich Text Plugins [Temporary Reference](https://www.mldoo.com/docs/simplepro/config/editor.html)

### Frequently Asked Questions
* Static files [temporary reference](https://www.mldoo.com/docs/simplepro/faq/static.html)
* Installation problems [temporary reference](https://www.mldoo.com/docs/simplepro/faq/install.html)
* Installation problems [temporary reference](https://www.mldoo.com/docs/simplepro/faq/install.html)

### Installation
#### pip installation
```shell
pip install DjangoAsyncAdmin
```
>If your installation is slow, you can use the mirror provided by the University of Science and Technology of China to speed up
```shell
pip install DjangoAsyncAdmin -i https://pypi.mirrors.ustc.edu.cn/simple/
```
#### Source code installation
##### 1. Clone the project to local
```shell
git clone https://github.com/Haoke98/DjangoAsyncAdmin.git
```
##### 2. Generate installation package
Enter the project root directory

```shell
python setup.py sdist bdist_wheel
```

##### 3. Install

```shell
pip install /path/to/your_project/dist/DjangoAsyncAdmin-6.5.4.tar.gz
```

Note: ⚠️ Replace `/path/to/your_project` with your project path (relative path/absolute path)

## Directory structure description

| Directory    | Remarks                            |
|--------------|-----------------------------------|
| bawa         |                                   |
| components   | Components, store model fields and form fields
| editor       | Editor, MD editor, UE rich text editor, JSON editor, etc.
| group        |                                   |
| locale       | Multiple language package directory, plaintext and binary files do not need to be processed
| management   |                                   |
| monitor      |                                   |
| static       | Static resource directory, no need to process
| templates    | Template directory, no need to process
| templatetags |                                   |
| \_\_init\_\_.py  |                            |
| action.py    |                                   |
| apps.py      |                                   |
| apps.py         |                            |
| conf.py      |                                   |
| conf.py         |                            |
| core.so      | Converted and saved to core.py
| decorators.py|                                   |
| dialog.py    |                                   |
| filters.py   |                                   |
| forms.py     |                                   |
| hanlers.py   | Removed the part that loads the core.so file and added `from core.py import *`
| middlewares.py|                                 |
| models.py    | Basic model file                  |
| urls.py      |                                   |
| utils.py     |                                   |

## New feature log
<table>
<tr>
<td>Version</td><td colspan="2">Description</td>
</tr>

<tr>
<td rowspan="1">6.7.3</td>
<td colspan="2">Fixed rendering abnormalities on the password component (PasswordInputField).</td>
</tr>

<tr>
<td rowspan="2">6.7.2</td>
<td colspan="2">Implemented the Json editor (JsonTextField) and password generator Input (PasswordInputField) and other components. At the same time, the component directory structure was preliminarily adjusted to improve the readability of the code.</td>
</tr>
<tr>
<td colspan="2"><img src="https://haoke98.github.io/DjangoAsyncAdmin/static/json_text_field.png"/></td>
</tr>



<tr>
<td rowspan="2">6.7.1</td>
<td colspan="2">Added the PasswordFormField form fields with copy and automatic password generation.</td>
</tr>
<tr>
<td colspan="2"><img src="https://haoke98.github.io/DjangoAsyncAdmin/static/截屏2023-11-15%2016.20.58.png"/></td>
</tr>


<tr>
<td>6.7.0</td>
<td colspan="2">Added basic classes BaseModel and BaseModelWithShowRate to reduce the repetitive design of some basic fields and attributes during the development process, and improve the efficiency of designing models.</td>
</tr>


<tr>
<td>6.6.0</td>
<td colspan="2">Removed the authorization and activation state validation mechanism to make it fully authorized, activated, and free to use for academic research. You can also apply for a free commercial use license. For licensing, cooperation, and other issues, please contact <1903243975@qq.com>.</td>
</tr>


<tr>
<td rowspan="2">6.5.4</td>
<td colspan="2">Upgraded and optimized the display of the title and LOGO on the login page of the background management.</td>
</tr>
<tr>
<td><img src="https://haoke98.github.io/DjangoAsyncAdmin/static/%E6%88%AA%E5%B1%8F2023-10-07%2005.15.43.png"/></td>
<td><img src="https://haoke98.github.io/DjangoAsyncAdmin/static/%E6%88%AA%E5%B1%8F2023-10-07%2005.04.21.png"></td>
</tr>

<tr>
<td>6.5.3</td>
<td colspan="2">Implemented the effect that the table header and the total column at the bottom of the table list page are fixed and the table bodyscroll.</td>
</tr>

</table>

## Open source license

The code in this repository is open source under the Apache-2.0 license. This project is completely open to academic research and can also apply for a free commercial use license. For licensing, cooperation, and other issues, please contact <1903243975@qq.com>.

## Acknowledgments & References

Thanks to [newpanjing](https://github.com/newpanjing/simpleui) for simpleui

Thanks to [newpanjing](https://github.com/newpanjing/simplepro) for simplepro