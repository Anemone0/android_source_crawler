# Android 项目源码爬虫
## 简介
在github上抓取Android项目源代码，用于进一步分析。
爬虫以git上的一个项目为start url，通过该url抓取star该项目的用户，在通过该用户找到更多Android项目。

## 用法
```bash
scarpy main.py
```

## 抓取结果
抓取到的项目简介每条以json格式保存在item.json文件中，项目源代码以zip格式保存在zips文件夹下。
