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

## 高级SQL

要点:

- 三值逻辑
	- `OR`:
		- `(unknown OR true) = true`
		- `(unknown OR false) = unknown`
		- `(unknown OR unknown) = unknown`
	- `AND`:
		- `(true AND unknown) = unknown`
		- `(false AND unknown) = false`
		- `(unknown AND unknown) = unknown`
	- `NOT`:
		- `(NOT unknown) = unknown`
- 空值
	- 任何含有`NULL`的表达式的结果是`NULL`
    - 任何含有`NULL`的比较的结果是`unkown`
    - 如果`WHERE`表达式的结果是`unkown`, 则会被当作`false`处理	

## 关系代数

要点:

- [operator](/database/relational-algebra/#operator), unary operator, binary operator, 特别注意选择条件操作符AND`^`, OR`∨`
- [join](/database/relational-algebra/#join), 搞懂笛卡尔积, 条件连接, 等值连接, 自然连接的层级关系, 特别注意条件连接中的内连接, 左外连接, 右外连接, 全连接的区别
- [union](/database/relational-algebra/#set)
- [logical query optimization](/database/query-processing/#logical-query-optimization), 主要思想就是使中间的结果尽量小

## 完整性约束

要点:

- 完整性约束: 不是所有时刻都会满足完整性约束, 可能在事务执行的过程中不满足. 在执行完整性约束修改/添加命令的时候, 如果数据库的状态满足该约束, 则顺利添加; 若不满足, 则命令会被拒绝.
- 域约束: `DEFAULT`, `NOT NULl`, `NULL`, 可以使用`CREATE DOMAIN`创建自定义域
- 键约束: `PRIMARY KEY`, `UNIQUE`, 主键默认是`NOT NULL`, `UNIQUE`
- 外键约束: 外键不能出现悬空引用. 可以选择的行为有`NO ACTION`, `CASCADE`, `SET NULL`, `SET DEFAULT`, 设置在`FOREIGN KEY ... REFERENCES ...`之后
- 语义约束: 和域约束最明显的区别就是语义约束是附在属性定义后的(有一个逗号), 而域约束和属性定义是在同一行上的
- 约束检查时间: 想象一个开关, 打开是`DEFERABLE`, 关闭是`NO DEFERABLE`(默认), 开了之后还可以选择一开始是否推迟, `INITIALLY DEFERED`还是一开始不推迟`INITIALLY IMMEDIATE`, 选择了一开始的状态之后, 分别可以进一步选择在执行的时候是否推迟, 分别是`SET CONSTRAINTS IMMEDIATE`还是`SET CONSTRAINTS DEFERRED`
- 断言: 这个期中考考了. 看那个[航海俱乐部的例子](/database/integrity-constraints/#assertion). 貌似还挺重要的, 格式为`CREATE ASSERTION <assertion_name> CHECK NOT EXIST (<select clause>)`
- 触发器: 由事件, 条件, 行动组成. 分为行级触发器和语句级触发器, 如果你的语句更新了多行数据, 那么行级触发器针对每行都会触发一次, 而语句级触发器是执行多少SQL语句执行几次触发器, 写法分别是`FOR EACH ROW`, `FOR EACH STATEMENT`. 触发器的写法为`CREATE TRIGER <triger_name> BEFORE/AFTER INSERT/UPDATE/DELETE (OF <attribute>) ON <table>`, `OF <attribute>`的写法只有`UPDATE`能用

## 规范化

要点:

- 三种异常: update anomaly, delete anomaly, insert anomaly. must update all records; will remove that room if every one drops that uos; can not reserve a room before student choosing
- 函数依赖: 一对一的关系, 使用armstrong公理, reflexivity, augmentation, transitivity, 特别注意reflexitivity, 如果右侧的属性包含在左侧中, 则称为"trivial functional dependency", 反之为"non-trivial functional dependency", 会使用该公理推导出函数依赖闭包
- 非主属性和主属性: 若属性不是候选键的一部分, 则为非主属性, 反之为主属性
- 完全/部分函数依赖: 若有X -> Y, 但是X的一部分无法推导出Y, 则为完全函数依赖, 反之为部分函数依赖
- 属性闭包: 用于判断是否为超键和候选键, 如果闭包的结果包含所有的属性, 则为超键, 如果与此同时, 其任何真子集都不是超键, 则它为候选键
- 第一范式: 每个字段为不可再分的原子值
- 第二范式: 没有部分依赖, 必须完全依赖于主键
- 第三范式: 非主属性不能依赖于其他非主属性
- Boye-Codd范式: 依赖的左侧必须是超键, 也就是说左侧不能是非主属性
- 第四范式: 用来处理多值依赖, 如名字和专业, 名字和语言
- 分解: 第一步, 检查分解后的属性闭包是否和原始闭包相等, 如三个属性A, B, C, 函数依赖为A -> B, B -> C, A -> C, 分解为(B, C), (A, B), 由于分解后的属性闭包为B -> C, A -> B, 利用传递依赖A -> C, 所以和原始的闭包相等; 第二步, 检查是否是无损连接, 它两的交集是否能推出其中的任意一个表. 如第一个表(A, B), 第二个表(B, C), 由于它们的交集B能够推出(B, C), 所以是无损连接

相关知识点:

- [functional dependencies closure](/database/normalization/#functional-dependency-closure)
- [attributes closure](/database/normalization/#属性闭包)

## 事务

要点: 

- ACID: Atomocity, Consistency, Isolation, Durability. 原子性; 事务开始和结束之后, 一致性没有被破坏; 并发调度的结果和串行调度的结果相同; 事务结束后, 数据能够persist
- 事务怎么用SQL写: `COMMIT`和`ROLLBACK`的使用
- 串行调度和可串行化调度: 串行调度是事务按照串行顺序执行的调度, 可串行化调度是调度进行转换后等价于可串行调度
- 三种问题: lost update, temporary update, incorrect summary. 事务B覆盖了事务A的更新; 读取了回滚前的数据; 在进行aggregation的时候读取了部分数据
- 隔离等级: read uncommited; read committed, repeatable read, serializable; 特别注意第三个, 其他事务只能看到事务提交之前的数据, 后三种隔离分别能解决temporary update, incorrect summary, lost update问题
- 冲突等价调度: 每一对冲突的操作在两个调度中都相同, 则它们冲突等价. 可以通过调换不冲突操作的顺序确定两个调度是否冲突等价, 如果一个调度冲突等价于一个串行调度, 则为冲突可串行化调度. 可以使用优先图来判断, 每个事务都是一个节点, 若一对冲突操作中事务A在事务B前面, 则从事务A到事务B有一条有向边. 若不存在环, 则调度就是冲突可串行化的. 冲突可串行化一定可串行化, 但是可串行化不一定冲突可串行化. 
- 优先图转为串行化方案: 必须保持原有的方向性, 没有箭头的可以调换顺序
- `UPDATE ... WHERE ...`这个语句包含了两个步骤, 首先根据条件读取, READ, 然后写入, WRITE; 普通的`SELECT`语句只有READ(幻灯片p34)

相关知识点:

- [ACID](/database/transaction/#acid)
- [serial/nonserial schedule; serializable/nonserializable schedule](/database/transaction/#调度)
- [problems without isolation](/database/transaction/#problems)
- [levels of isolation](/database/transaction/#隔离级别)
- [type of conflicts](/database/transaction/#conflicts)
- [conflict serializability](/database/transaction/#冲突可串行化调度)

怎么做冲突可串行化的题:

1. 找到存在冲突的操作, 要求是不同的事务, 同一个数据, 其中一个操作是写
2. 确定没对冲突的顺序, 是谁在前面, 谁在后面
3. 事务体现为一个节点, 顺序体现为箭头的方向
4. 如果图是无环的, 则说明是冲突可串行化的
5. 若为冲突可串行化, 根据优先图, 可以调换两者之间不存在箭头的事务的顺序, 得到数个串行化调度

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
