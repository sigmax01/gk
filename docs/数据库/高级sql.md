---
title: 数据库:高级SQL
comments: true
---

## 嵌套查询

???+ example "例子"

    如[图](https://img.ricolxwz.io/056fd74701e82526e4b043f255c469ee.png)是一张学生表和参与课程表, 现在要你找到同时参加COMP5138和ISYS3207的学生的名字, 下列查询是否正确?

    ```sql
    SELECT name FROM Student NATURAL JOIN Enrolled WHERE uos_code='COMP5138'
    INTERSECT
    SELECT name FROM Student NATURAL JOIN Enrolled WHERE uos_code='ISYS3207'
    ```

    注意, 上述查询操作是错误的. 第一个查询会返回Adam, Lily; 第二个查询返回Lily, Adam. 最后的结果是Lily, Adam. 但是, 问题是, Lily是同一个Lily, Adam不是同一个Adam. 第一个查询返回的是来自澳大利亚的Adam, 第二个查询返回的是德国的Adam, 实际上, 无论是哪一个Adam都没有同时参与两门课, 只是两个人名字碰巧一样罢了.

    解决这个问题的方法是使用嵌套查询, 即先基于sid选出同时参加两门课程的学生, 然后根据sid选出学生的名字.

    ```sql
    SELECT name
    FROM Student
    WHERE sid IN (
        SELECT sid FROM Enrolled WHERE uos_code='COMP5138'
        INTERSECT
        SELECT sid FROM Enrolled WHERE uos_code='ISYS3207'
    )
    ```

### 集合比较操作

SQL中用于子查询的集合比较操作有四种:

- `v [NOT] IN R`: 判断值`c`是否在结果集合`R`中, 或者加上`NOT`, 判断是否不在集合中
- `[NOT] EXISTS R`: 判断子查询`R`的结果集是否为空, `R`不为空为真, 或者`NOT`为空为真
- `v op ALL R`: `op`是一个比较运算符, `v`对`R`中每个元素的比较都成立则为真
- `v op SOME R`: `op`是一个比较运算符, `v`至少对`R`中的一个元素比较成立则为真

???+ example "例子"

    === "例子1"

        ```sql
        SELECT sid
        FROM Enrolled
        WHERE marks >= ALL (SELECT marks
                            FROM Enrolled)
        ```

    === "例子2"

        ```sql
        SELECT name
        FROM Student
        WHERE sid NOT IN (SELECT sid
                          FROM Enrolled
                          WHERE semester='2024-S2')
        ```

### 视图

视图, View是数据库中的一种虚拟表. 它并不直接存储数据, 而是通过一条SQL查询定义的. 视图可以像普通表一样被查询, 但是它实际上是一个查询的结果集, 只有在使用的时候才会执行相应的查询操作. 视图的主要作用有:

- 抽象化: 通过视图可以简化复杂的查询, 将多个表的复杂查询封装为一个虚拟表
- 安全性: 通过视图可以控制用户访问的权限, 只让用户看到部分数据, 隐藏表中的其他信息
- 复用性: 将频繁使用的查询逻辑封装为视图, 方便多次调用, 无需每次重写复杂的查询语句

???+ example "例子"

    ```sql
    CREATE VIEW student_enrollment AS
            SELECT sid, name, title, semester
            FROM student NATURAL JOIN Enrolled NATURAL JOIN unitofstudy
    ``` 

## 聚合操作

SQL支持数种聚合操作. 包括`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`, 除了`COUNT`之外, 所有的聚合操作都是用于单一属性的. 注意, 这些操作会应用于所有的重复项中, 除非使用`DISTINCT`声明.

???+ example "例子"

    === "例子1"

        如[图](https://img.ricolxwz.io/b1d7089b238fb3a10cd0a4710cb3ed80.png).

    === "例子2"

        如[图](https://img.ricolxwz.io/e30cc90ccbccf965e719d51600e99369.png).

    === "例子3"

        如[图](https://img.ricolxwz.io/9d439950a11be954151f5ffcc2212d27.png).

### 分组

除了对一个属性中进行聚合之外, 有时我们需要用`GROUP BY`对该属性下的某些组进行聚合.

???+ example "例子"

    如[图](https://img.ricolxwz.io/b1a1edec3f4d45f040fc471d6858c7e9.png). 这里, Sales表格可以分为IBM和DELL, 我们对company进行分组, 用`GROUP BY`关键字, 然后会对IBM的amount, DELL的amount分别进行聚合, 而不是整一个属性amount进行聚合.

#### 过滤

我们可以对`HAVING`子句对分组的结果进行过滤, 如`HAVING SUM(amount) > 10000`来筛选出销售总额大于`10000`的公司. 需要注意的是, 在`SELECT`或者`HAVING`子句中的字段必须是聚合函数的结果或是出现在`GROUP BY`子句中的字段. 

## 评估流程

评估流程如[图](https://img.ricolxwz.io/549b2dcf48909f15ac8c06a30396c35f.png)所示.

???+ example "例子"

    如[图](https://img.ricolxwz.io/91083d1329e274f2bb2ae9ad93942e52.png)--->[图](https://img.ricolxwz.io/c0f6aab1c5ef2e998cb5a7f64e7133b1.png).

