---
title: 容器:dockerfile
comments: true
---
    
## `ENTRYPOINT`&`CMD`

`ENTRYPOINT`定义了容器启动时启动的主命令. `docker run`容器启动的时候, `ENTRYPOINT`指令不会被忽略, 除非使用`--entrypoint`选项. 即使用户在启动容器的时候传递了参数, 也会将参数附加到`ENTRYPOINT`声明的命令后面, 而不是覆盖它, 但是`CMD`定义的参数会被覆盖. 

`CMD`在`ENTRYPOINT`存在的时候, 用于为`ENTRYPOINT`提供默认的参数, 如果启动时提供了参数, `CMD`中的参数会被覆盖. 如果`ENTRYPOINT`不存在, `CMD`指令将用于定义容器启动时的默认命令, 若用户在启动容器的过程中没有提供其他命令, 会执行`CMD`中定义的内容.