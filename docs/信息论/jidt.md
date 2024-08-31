---
title: 信息论:JIDT
comments: true
---

JIDT, Java Information Dynamics Toolkit, 是一个GPL v3授权的用于复杂系统信息处理过程中理论性的信息测量. 由本节课的教授[Joseph T.Lizier](https://www.sydney.edu.au/engineering/about/our-people/academic-staff/joseph-lizier.html)开发. 原文: [https://arxiv.org/abs/1408.3270](https://arxiv.org/abs/1408.3270). 软件: [https://github.com/jlizier/jidt/](https://github.com/jlizier/jidt/).

## 安装

JIDT由Java写成, 但是可以在Matlab/Octave, Python, R, Julia, Clojure等语言中直接使用. JIDT几乎不需要安装, 只需要安装一个JVM(JVM还不够吗???). 安装过程如下:

1. 安装OpenJDK: 前往[https://jdk.java.net/](https://jdk.java.net/), 下载对应版本的OpenJDK, 然后放到对应的位置, 参考[https://github.com/supertokens/supertokens-core/wiki/Installing-OpenJDK-for-Mac-and-Linux](https://github.com/supertokens/supertokens-core/wiki/Installing-OpenJDK-for-Mac-and-Linux)
2. 前往仓库, 下载对应版本的安装包[https://github.com/jlizier/jidt/releases](https://github.com/jlizier/jidt/releases) 
3. 解压安装包, 运行infodynamics.jar

若需要在Python中运行Java, `pip install jpype1`.