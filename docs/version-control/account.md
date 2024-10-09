---
title: 版本控制:账户
comments: true
---

## 配置邮箱和用户名

可以设置全局邮箱和用户名:

```bash
git config --global user.name <username>
git config --global user.email <useremail>
```

可以取消设置全局邮箱和用户名:

```bash
git config --global --unset user.name
git config --global --unset user.email
```

也可以设置单个Git项目的邮箱和用户名:

```bash
git config user.name <username>
git config user.email <useremail>
```

注意, 这里设置的邮箱和用户名仅仅影响的是提交记录中的作者信息, 不会影响代码克隆/推送等操作的时候用到的Git账户, 克隆/推送等时候用到的Git账户完全由SSH配置时候的密钥和Host和仓库名决定.

如我现在要以`wexu0327`的身份克隆`ricolxwz`下的`5318`仓库. 首先, 必须确认`wexu0327`拥有`ricolxwz`的`5318`仓库的访问权. 然后, 使用`wexu0327`的私钥`~/.ssh/id_ed25519_2`和`github.com`服务器建立连接, 然后, 再克隆仓库: `git clone gh2:ricolxwz/5318.git`. 这个时候, 我们可以在克隆好的`5318`仓库内设置Git邮箱用户名: 

```bash
git config user.name wenzexu # 可以注意到, Git账户名是和Github账户名两个完全不同的概念
git config user.email ricol.xwz@hotmail.com
```

## 配置Git-SSH

Git-SSH是建立在SSH之上的一种加密通讯方式, 它的底层使用的是SSH, 但是在上层有所不同. 

### 原理

Git-SSH常用于连接远程仓库, 以克隆为例`git clone git@github.com:ricolxwz/gk.git`, 这个过程中, Git会发现你要连接的是`github.com`服务器, 以`git`为用户名, 这个时候就会调用底层的SSH服务尝试连接, `github.com`服务器会给你发送它的公钥, 防止中间人攻击, 你在终端输入yes回车之后, 服务器的公钥指纹会放在你的`known_hosts`文件中, `github.com`服务器会检查你的公钥是不是和你在Github账户里添加的公钥匹配, 如果匹配, 就连接成功, 然后会根据你提供的仓库路径`ricolxwz/gk.git`将这个仓库传输给你.

### `~/.ssh/config`

`~/.ssh/config`这个文件用来配置底层的SSH服务, 文件由多个`Host`块组成, 每个块定义一个连接配置, 基本格式如下:

```
Host <alias>
    HostName <host_name>
    User <user_name>
    Port <port>
    IdentityFile <priv_key>
    ForwardAgent <yes/no>
    ProxyCommand <proxy_command>
    PreferredAuthentications <auth_method>
```

- `Host`: 为主机指定一个别名
- `HostName`: 实际的主机名或者IP地址
- `User`: 登录的用户名
- `Port`: SSH端口号
- `IdentityFile`: 指定私钥文件的路径
- `ForwardAgent`: 是否开启SSH转发, 通常结合跳板机使用, 会见给你的身份代理连接转发到远程服务器
- `ProxyCommand`: 指定一个命令, SSH将通过这个命令建立到目标主机的连接, 而不是直接连接
- `PreferredAuthentications`: 尝试认证时的认证方法顺序, 可选`publickey`, `password`, `keyboard-interactive`, `gssapi-with-mic`

我们可以设置一个别名, 然后下次克隆的时候就不用写`git@github.com`, 只需要写`git clone gh:ricolxwz/gk.git`:

```
Host gh
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

可以利用这个文件轻松实现在同一个电脑上拥有两个不同的Git身份:

```
Host gh1
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_1

Host gh2
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_2
```