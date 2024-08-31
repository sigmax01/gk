---
title: 信息论:SQL
comments: true
---

???+ info "信息"

    省略所有的例子边框.

[关系代数](/数据库/关系代数)是一种理论基础的过程式的查询语言, 可能比较难以理解并且不是专家的话使用起来非常困难. 这个时候, SQL来了, 它是一种高阶的声明式的查询语句, 即它只描述我们感兴趣的数据, 而不是怎么取到它. 它基于SEQUEL, 作为IBM公司的查询语句在1970年中期发明. SQL在内部会将查询语句映射到相应的关系代数表达式, 见[结构图](/数据库/关系代数/#RA在RDBMS中的角色).

## SQL构成

数据库管理系统(DBMS)中的操作通常分为三大类: 

- 数据定义语言, DDL, 主要用于定义和管理数据库结构, 常见的操作包括`CREATE`, `ALTER`, `DROP`等等...
- 数据操作语言, DML, 主要用于查询和修改数据库中的数据, 常见的操作包括`SELECT`, `INSERT`等等...
- 数据控制语言, DCL, 主要用于控制对数据库的访问权限, 常见的操作包括`GRANT`, `REVOKE`等等...

DDL, DML和DCL都是SQL的子集或组成部分.

## 基础SQL查询

### 关键字

基础SQL查询的常用关键字有:

- `SELECT`: 列出所有从查询中返回的列
- `FROM`: 指明查询数据的来源的表
- `WHERE`: 指明包含在查询结果中元组的条件
- `ORDER BY`: 指明查询结果的排序

### Select-From-Where (SFW) 查询

SFW查询的格式为:

```sql
SELECT <attributes> FROM <one or more tables> WHERE <conditions>
```

- 列出所有学生的姓名: `SELECT name FORM Student`
- 列出所有中国学生的名字: `SELECT name FROM Student WHERE country="CN"`
- 列出所有的属性: `SELECT * FROM Student`

SFW查询语句背后执行的是下列关系代数表达式: `πA1,A2,...,An(σΘ(R1×R2×...×Rm))`.

- `SELECT`对应的是投影π
- `FROM`对应的是笛卡尔积R1×R2×...×Rm
- `WHERE`对应的是选择σ

???+ tip "Tip"

    - SQL语句对大小写不敏感
    - 对于字符串使用单引号
    - 字符串对大小写是敏感的\pi
    - SFW返回的结果也是关系/表
    - SFW返回的结果表中可以包含重复元组, 事实上, RDBMS在任何表中都可以允许存在重复值的. SFW返回的结果会保留原始数据中重复的元组, 如果要使返回的表中不含有任何的重复元组的话, 可以使用`DISTINCT`命令, 如`SELECT DISTINCT country FROM Student`
    - 可以包含算数运算, 如`SELECT uos_code, title, points*2 FROM UnitOsStudy`
    - `WHERE`语句后面包含条件, 可以使用逻辑运算符, 如`>`, `AND`等
    - SQL包含了一个字符串匹配机制, 类似于正则表达式. 我们可以使用`LIKE`来实现字符串的匹配. 如列出所有包含`COMP`的课程`SELECT title FROM UnitOfStudy WHERE uos_code LIKE 'COMP%'`. `%`表示匹配任何子字符串, `_`表示匹配任何单字符
    - SQL支持不少的字符串操作, 如`||`表示拼接字符串, 可以将字符串从大写转化为小写, 取出字符串长度, 切片等等
    - SQL支持对属性进行重命名, 注意, 这只是对结果表生效, 无法改变原表的属性名称. 使用`AS`来实现. 如`SELECT a.uos_code AS course_code, a.credit_points FROM UnitOfStudy a WHERE a.uos = 'COMP5318'`
    - SQL支持对某一列进行排序, 使用`ORDER BY`语句.. 如`SELECT name FROM Student WHERE country='CN' ORDER BY name`. 注意有两个方向, 一个是`ASC`, 表示升序(默认), 一个是`DESC`, 表示降序. 可以在`ORDER BY`语句后面声明是降序还是升序, 如`ORDER BY country DESC, name ASC`
    - SQL支持使用表的别名, 如`SELECT L.name, M.name FROM Lecturer L, Lecturer M, L.manager = M.empid`, 在这种情况下, `L`和`M`表示的其实是同一张表, 可以将其想象为`Lecturer`表的不同的两份副本

## 连接查询

连接在SQL语句中分为隐式连接和显式连接. 

### 隐式连接

隐式连接使用到的是`FROM`和`WHERE`语句, `FROM`语句用于列出参与到查询中的表, 对应的是笛卡尔积中的表, 连接的条件在`WHERE`语句中列出. 如选出Student表和UnitOfStudy的笛卡尔积: `SELECT * FROM Student, UnitOfStudy`. 如[图](https://cdn.jsdelivr.net/gh/sigmax0124/img@master/2024/08/109682364bd058e45fc66e1c06fa8291.png).

### 显式连接

默认连接用到的是内连接, 关于四种连接的区别, 请见[这里](/数据库/关系代数/#条件连接). 显式连接用到的是`FROM`, `JOIN`和`ON`关键字.

## 集合操作

SQL语句中, `UNION`, `INTERSECT`, `EXCEPT`对应的是集合操作中的∪, ∩和−. 

???+ tip "Tip"

    要注意的是, 上述这几种操作会自动去除重复, 内部的原理是在操作之前会消除掉输入表的重复行, 然后再做集合操作. 如, 假设一个元组在R中出现了3次, 在S中出现了1次, 那么R-S这个操作之后的结果中将不含有这个元组. 若要保留所有的重复行, 则分别需要用到`UNION ALL`, `INTERSECT ALL`和`EXCEPT ALL`. 如, 假设一个元组在R中出现了m次, 在S中出现了n次, 那么:

    - 在`R UNION ALL S`的结果中会出现m+n次
    - 在`R INTERSECT ALL S`的结果中会出现min(m, n)次
    - 在`R EXCEPT ALL S`的结果中会出现max(0, m-n)次

例子如[图1](https://cdn.jsdelivr.net/gh/sigmax0124/img@master/2024/08/4ed0a2e07f06c175ee79d5858f3bca9a.png), [图2](https://cdn.jsdelivr.net/gh/sigmax0124/img@master/2024/08/ffa4171300b7c1ba9b17000bf4a96476.png).