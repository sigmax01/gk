---
title: 数据库:考点
comments: true
---

个人认为的大题考点, 由于小题占比过小不提供, 并且, **只写重点, 不写非常基础的东西**.

## 数据模型

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

## 关系模型

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

## 关系代数

相关知识点:

- [operator](/database/relational-algebra/#operator), unary operator, binary operator, 特别注意选择条件操作符AND`^`, OR`∨`
- [join](/database/relational-algebra/#join), 搞懂笛卡尔积, 条件连接, 等值连接, 自然连接的层级关系, 特别注意条件连接中的内连接, 左外连接, 右外连接, 全连接的区别
- [union](/database/relational-algebra/#set)
- [logical query optimization](/database/query-processing/#logical-query-optimization), 主要思想就是使中间的结果尽量小

## 规范化

相关知识点:

- [functional dependencies closure](/database/normalization/#functional-dependency-closure)
- [attributes closure](/database/normalization/#属性闭包)

## 事务

相关知识点:

- [ACID](/database/transaction/#acid)
- [serial/nonserial schedule; serializable/nonserializable schedule](/database/transaction/#调度)
- [problems without isolation](/database/transaction/#problems)
- [levels of isolation](/database/transaction/#隔离级别)
- [type of conflicts](/database/transaction/#conflicts)
- [conflict serializability](/database/transaction/#冲突可串行化调度)

## 存储与索引

要点:

- 阻塞因子: 块大小/记录大小, 若<1, 则发生"记录跨块"
- LRU和MRU算法: LRU, 替换掉最久未使用的数据块; MRU, 替换掉最近使用的数据块
- 文件和页面: 一张表对应一个文件, 一个文件对应数个页面, 一个页面对应一个或多个块. 若一个页面为4k, 页头固定250字节元数据, occupancy为80%, 则每页有(4k-250)*0.8=3076字节来存储数据, 设每个记录的大小为200字节, 则向下取整后可以存储15条数据. 假设该文件有2000000条记录, 则总共需要的页数为2000000/15向上取整为133334页. 实际占用空间为4k\*133334=546136064字节, overhead为(546136064-400000000)/400000000=36.53%
- 三种文件组织: 无序文件, 排序文件, 索引文件
- 访问路径: 线性扫描(很慢, 基本要扫描一半的页), 二分扫描(维护成本很高), 索引扫描
- B+树: 假设表存储在140351个页面的文件中, 页面按照逻辑排序(物理上不一定连续), 索引条目由搜索键和行指针构成, 共8字节. 假设每页的总可用空间为3846字节, 填充因子为75%, 则向下取整后可以存放360条索引. 最底层索引总共需要140351个, 所以需要的索引页数向上取整后为390页. 对于这个390页索引页, 在它的基础上继续套娃建立索引, 那么需要390/360向上取整2页来存放, 继续套娃, 最顶层只需要1页. 所以索引页的总数为393. 相对于140351个数据页, 仅仅增加了0.2%的需求. 在查询的时候, 只需要存放3个索引页和1个数据页入内存, 也就是4次IO
- 复合索引: 用于索引的键由多个属性构成, 要特别注意排序的顺序, 如先按照age排序, 然后按照salary排序, 那么就要先搜索age, 再搜索salary, 不能跳过age搜索salary

相关知识点:

- [block factor](/database/storage-indexing/#blocking-factor)
- [LRU & MRU](/database/storage-indexing/#buffer-management)
- [file & page](/database/storage-indexing/#organization-storage)
- [file organisation](/database/storage-indexing/#file-organisation)
- [access path](/database/storage-indexing/#access-path)
- [B+ tree](/database/storage-indexing/#bp-tree)

## 查询处理

要点:

- 嵌套循环连接: b_R+|R|*b_S, R是外表, |R|是R元组的数量, b是页数
- 块嵌套循环连接: b_R+b_R*b_S, R是外表, b是页数
- 索引嵌套循环连接: b_R+|R|*c, R是外表, c是对S表索引的平均成本
- 外部合并排序: 建议考试前复习一下PPT上的那个例子
- 评估策略: Materialization和Pipelining, 前者把中间结果存储到一个临时关系中, 供后续使用, 后者是直接将输出传递给下一个操作

相关知识点:

- [nested loop join](/database/query-processing/#nested-loop-join)
- [block nested loop join](/database/query-processing/#block-nested-loop-join)
- [index nested loop join](/database/query-processing/#index-nested-loop-join)
