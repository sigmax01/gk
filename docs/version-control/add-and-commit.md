---
title: 版本控制:添加和提交
comments: true
---

## 添加

可以通过`git add <file>`添加文件到暂存区, 或者通过`git add .`添加所有当前目录的文件. 还可以通过`git rm --cached <file>`命令将文件从暂存区中移出. 或者可以使用通配符添加, 如`git add *.txt`. 可以通过`git status`查看暂存区的情况

## 提交

可以通过`git commit -m <message>`提交到仓库中, 只会提交暂存区中的文件. 可以通过`git log`查看提交记录.