---
title: 版本控制:配置
comments: true
---

## 配置文件路径

当前项目的Git配置一般都在`./.git/config`文件里面, 全局的Git配置一般在`~/.gitconfig`文件里.

## 命令

### `get config --list`

可以通过`git config --list`查看当前的Git项目的配置, 如:

```bash
$ git config --list
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
remote.origin.url=gh2:ricolxwz/5318.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.master.remote=origin
branch.master.merge=refs/heads/master
```

### `get config -e <--global>`

可以通过`get config -e <--global>`设置当前Git项目的配置或者全局配置, 如:

```bash
$ git config [--global] user.name "wenzexu"
$ git config [--global] user.email "ricol.xwz@outlook.com"
```

修改的是全局配置.
