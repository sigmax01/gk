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