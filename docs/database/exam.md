---
title: 数据库:考点
comments: true
---

个人认为的大题考点, 由于小题占比过小不提供, 并且, **只写重点, 不写非常基础的东西**.

- 画ERD

    要点:

    - 如何表示属性, 包括它的主键(实线), 外键(虚线); 复合属性(多个椭圆连接到一个大椭圆); 区分符(虚线); 派生属性(虚线椭圆); 多值属性(双椭圆形)
    - 如何表示约束, 包括键约束(箭头), 参与约束(粗线), 键约束和参与约束的结合(粗线箭头), 以及基数约束(小数字)
    - 如何表示实体, 包括强实体(矩形), 弱实体(双矩形). 
    - 如何表示关系, 包括普通的实体之间的关系(菱形), 强弱实体之间的关系(双菱形)
    - 如何表示isA关系(三角形)

    注意点:

    - 一般不会在ERD中标注出关系集的键, 只会标注实体集的键
    - 看到at most, 立马联想到键约束, 画一条箭头
    - 看到at least, 立马联想到参与约束, 画一条粗线
    - 看到exactly one, 立马联想到键约束+参与约束, 画一条粗线箭头

    相关知识点:

    - [degree](/database/conceptual-model/#degree), unary, binary, ternary relationship
    - [cardinality](/database/conceptual-model/#基数), 1-to-1, 1-to-many, many-to-many
    - [key constraints](/database/conceptual-model/#键约束)
    - [participation constraints](/database/conceptual-model/#participation-constraints)
    - [cardinality constraints](/database/conceptual-model/#基数约束)
    - [weak entity & strong entity](/database/conceptual-model/#强弱实体型)
    - [isA relationship](/database/conceptual-model/#泛化反泛化)
    - [aggregation](/database/conceptual-model/#aggregation)

- ERD转换为RM

    要点:

    - 如何映射没有任何约束的关系: 关系集独立建表, 两个实体集的主键的组合称为该新表的主键, 同时也是该新表的外键, 需要用箭头指到相应的实体集的主键, 如[图](https://img.ricolxwz.io/f7a07b8706af6f4dab96d5a946ee93a2.png)
    - 如何映射单侧有键约束的关系: 合并关系集和含有约束一侧实体集的属性, 并在这一侧实体集上加上一个外键, 指向另一侧实体集的主键, 如[图](https://img.ricolxwz.io/d528c111b390896090bb774e9fd92fab.png).
    - 如何映射双侧有键约束的关系: 在上面单侧键约束的基础上, 往一侧的实体集的外键上加一个唯一性约束, 如[图](https://img.ricolxwz.io/d528c111b390896090bb774e9fd92fab.png)
    - 如何映射双侧有键约束, 其中一侧还有参与约束的关系: 在上面双侧键约束的基础上, 往一侧的实体集的外键上加一个非空约束, 如[图](https://img.ricolxwz.io/fca7486e063b1bc75f1ef25d31873e46.png)
    - 如何映射强弱实体关系: 如[图](https://img.ricolxwz.io/fca7486e063b1bc75f1ef25d31873e46.png)
    - 如何映射isA关系: 如[图](https://img.ricolxwz.io/e24aee851049a321ea87670a3368daf6.png)

    注意点:

    - 强弱实体映射的时候, 外键同时也和区分符构成复合主键
    - 映射isA关系的时候, 外键同时也是主键

    相关知识点:

    - [map constraints](/database/relational-model/#map-constraints)
    - [map weak & strong entity](/database/relational-model/#map-weakstrongentity)
    - [map isA](/database/relational-model/#map-isa)
    - [map aggregation](/database/relational-model/#map-aggregation)

- 写关系代数

    相关知识点:

    - [operator](/database/relational-algebra/#operator), unary operator, binary operator, 特别注意选择条件操作符AND`^`, OR`∨`
    - [join](/database/relational-algebra/#join), 搞懂笛卡尔积, 条件连接, 等值连接, 自然连接的层级关系, 特别注意条件连接中的内连接, 左外连接, 右外连接, 全连接的区别
    - [union](/database/relational-algebra/#set)
    - [logical query optimization](/database/query-processing/#logical-query-optimization), 主要思想就是使中间的结果尽量小

- 确定调度是否冲突可串行化

	相关知识点:

	- [ACID](/database/transaction/#acid)
	- [serial/nonserial schedule; serializable/nonserializable schedule](/database/transaction/#调度)
	- [problems without isolation](/database/transaction/#problems)
	- [levels of isolation](/database/transaction/#隔离级别)
	- [type of conflicts](/database/transaction/#conflicts)
	- [conflict serializability](/database/transaction/#冲突可串行化调度)

- 计算函数依赖闭包, 属性闭包, 并根据结果判断是否为超键或者候选键

	相关知识点:

	- [functional dependencies closure](/database/normalization/#functional-dependency-closure)
	- [attributes closure](/database/normalization/#属性闭包)

- 优化连接操作, 计算IO次数

	相关知识点:

	- [nested loop join](/database/query-processing/#nested-loop-join)
	- [block nested loop join](/database/query-processing/#block-nested-loop-join)
	- [index nested loop join](/database/query-processing/#index-nested-loop-join)