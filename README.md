<div align="center">

# 在线教学平台小助手
基于selenium框架的在线教学平台自动化执行脚本<br><br>
[![madewithlove](https://img.shields.io/badge/made_with-%E2%9D%A4-red?style=for-the-badge&labelColor=orange
)](https://github.com/r0ut3r916/cep-hack)

![GitHub Release](https://img.shields.io/github/v/release/r0ut3r916/cep-hack)
![GitHub Repo stars](https://img.shields.io/github/stars/r0ut3r916/cep-hack)
![GitHub repo size](https://img.shields.io/github/repo-size/r0ut3r916/cep-hack)


</div>





## 声明

本项目为开源项目，开发团队的所有成员与本项目的所有开发者以及维护者（以下简称贡献者）对本项目没有控制力。本项目的贡献者从未向任何组织或个人提供包括但不限于api-key租用、硬件支持等一切形式的帮助；本项目的贡献者不知晓也无法知晓使用者使用该项目的用途。故一切基于本项目的违法、违规行为都与本项目贡献者无关。一切由此造成的问题由使用者自行承担。

1. 本项目是基于学术交流目的建立，仅供交流与学习使用，并非为生产环境准备。
2. 禁止贩卖本项目用于盈利，该项目维护者坚决抵制上述行为，不同意此条则禁止使用该项目。
3. 继续使用视为已同意本仓库 README 所述相关条例，本仓库 README 已进行劝导义务，不对后续可能存在问题负责。
4. 如果将此项目用于任何其他企划，请提前联系并告知本仓库作者，十分感谢。

## 更新内容
+ 修改登录逻辑以适配无法更改密码的账号
+ 刷完所有内容后添加挂机功能
+ 移除Deepseek生成讨论功能（恢复时间待定）



## 开始使用
### 直接启动
#### 环境配置
以下指令需在 Python 版本大于3.10的环境中执行。  
##### 1. 通过 pip 安装依赖
```bash
pip install -r requirements.txt
```
##### 2. 下载并安装chromedriver&&chrome-headless-shell
1. 在[Chrome for Testing 可用性检测网站](https://googlechromelabs.github.io/chrome-for-testing/)下载Stable版本的chromedriver和chrome(或chrome-headless-shell)
2. 将下载好的文件解压至脚本所在目录

##### 3. 运行脚本
使用以下指令以默认配置启动
```bash
python release.py
```
使用以下指令启动后浏览器窗口不会关闭
```bash
python release.py -n
```
使用以下指令启用旧版登录（账号密码登录）
```bash
python release.py -l
```
使用以下指令定义chromedriver路径
```bash
python release.py -d [chromedriver路径]
```
使用以下指令定义chrome或chrome-headless-shell路径
```bash
python release.py -d [chrome或chrome-headless-shell路径]
```


### 使用整合包
下载并解压`script_.7z`
#### Windows 用户
##### 默认配置
双击`release.exe`
##### 不使用大模型api-key
双击`不使用大模型api-key.bat`
##### 已有账号密码登录
双击`使用账号密码登录.bat`
##### 自动提交讨论
双击`自动提交.bat`
#### MacOS/Linux 用户
暂不支持整合包
