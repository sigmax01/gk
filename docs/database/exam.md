---
title: 数据库:考点
comments: true
---

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

## 关系模型 {#relational-model}

要点:

- 如何映射没有任何约束的关系: 关系集独立建表, 两个实体集的主键的组合称为该新表的主键, 同时也是该新表的外键, 需要用箭头指到相应的实体集的主键, 如[图](https://img.ricolxwz.io/f7a07b8706af6f4dab96d5a946ee93a2.png)
- 如何映射单侧有键约束的关系: 合并关系集和含有约束一侧实体集的属性, 并在这一侧实体集上加上一个外键, 指向另一侧实体集的主键, 如[图](https://img.ricolxwz.io/e65017767a761150a29e223fd8ea03dd.png).
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

## SQL

要点:

- 连接语句
	- 笛卡尔积: `FROM <table1>, <table2>`
	- 条件连接/等值连接: `FROM <table1> INNER/LEFT OUTER/RIGHT OUTER/FULL OUTER JOIN <table2> ON <condition>`, 只写一个JOIN默认是内连接
	- 自然连接: `FROM <table1> NATURAL JOIN <table2>`
- 条件语句
	- 整体框架: `WHERE <condition1> AND/OR <condition2>`
	- 条件: 可以是普通的大于等于小于某个值, 也可以和嵌套查询返回的结果比较, 常用的有`v NOT EXIST`, `NOT IN`, `v op ALL`, `v op SOME`
- 分组语句
	- 整体框架: `GROUP BY <group> HAVING <condition>`

执行的顺序为连接 -> 筛选(WHERE) -> 分组 -> 过滤(HAVING) -> 排序 -> 选择.

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
- **特别注意差**: 这个考的可能性很高, 因为在PPT和模拟考都出现了, 对应的是SQL语句条件判断的嵌套中的`v NOT IN`语句, 可以改写为π~attribute~-π~attribute~

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

怎么做判断是否为候选键的题: 

1. 判断它是否是超键: 通过Armstrong公理不断推出属性闭包, 如果该闭包中包含所有的属性, 则为超键
2. 判断它的真子集是否为超键: 写出它的真子集, 分别对这些真子集使用Armstrong公理写出属性闭包, 如果闭包中包含所有的属性, 则为超键, 只要有一个真子集是超键, 则原属性组合就不是候选键

怎么做MVD和4NF的题:

1. 如何检查是不是MVD: 如[图](https://img.ricolxwz.io/ef967f1ab99097e46abaf33cfec9cc6d.png), 对于任意两个UoS是COMP9120的记录, 存在另外两个UoS是9120的记录, 使得Textbook相同的情况下Tutor不同, Tutor相同的情况下Textbook不同. (然后还可以插入一条新的记录, 比如插入一个老师Lijun C, 则应该有两条记录, 对应两种Textbook)
2. 如何判断是否处于4NF: 满足下列条件中的任意一条 a. **所有**的多值依赖都是平凡多值依赖(Y ⊆ X或X ∪ Y = R, 特别注意第二个条件); b. **所有**的多值依赖中左侧是超键

怎么做范式的题:

1. 弄清楚2NF, 3NF, BCNF的概念, 分别是没有部分依赖, 非主属性不能依赖其他非主属性, 左侧是超键
2. 对于BCNF, 它可能会先给出很多函数依赖, 然后让你判断这些函数依赖是否符合BCNF, 那么判断的方法就是对于这些函数依赖的左侧, 用属性闭包判断其是否为超键, 如果是所有函数依赖的左侧都是超键, 则说明表符合BCNF
3. 执行分解: 如[图](https://img.ricolxwz.io/ba06d45ab84b9af2868b8fd73170af4b.png)
4. 检查分解: a. 检查分解后的函数依赖闭包是否和原始闭包相同或者函数依赖和原始函数依赖相同, 如[图](https://img.ricolxwz.io/180a82391d7abd8b74382f665b8a260e.png); b. 检查无损连接, 交集是否能够推出其中任意一个表, 即交集的属性至少是任意一个表的键

## 事务

要点: 

- ACID: Atomocity, Consistency, Isolation, Durability. 原子性; 事务开始和结束之后, 一致性没有被破坏; 并发调度的结果和串行调度的结果相同; 事务结束后, 数据能够persist
- 事务怎么用SQL写: `COMMIT`和`ROLLBACK`的使用
- 串行调度和可串行化调度: 串行调度是事务按照串行顺序执行的调度, 可串行化调度是调度进行转换后等价于可串行调度
- 三种问题: lost update, temporary update, incorrect summary. 事务B覆盖了事务A的更新; 读取了回滚前的数据; 在进行aggregation的时候读取了部分数据
- 隔离等级: read uncommited; read committed, repeatable read, serializable; 特别注意第三个, 其他事务只能看到事务提交之前的数据, 后三种隔离分别能解决temporary update, incorrect summary, lost update问题
- 冲突等价调度: 每一对冲突的操作在两个调度中都相同, 则它们冲突等价. 可以通过调换不冲突操作的顺序确定两个调度是否冲突等价, 如果一个调度冲突等价于一个串行调度, 则为冲突可串行化调度. 可以使用优先图来判断, 每个事务都是一个节点, 若一对冲突操作中事务A在事务B前面, 则从事务A到事务B有一条有向边. 若不存在环, 则调度就是冲突可串行化的. 冲突可串行化一定可串行化, 但是可串行化不一定冲突可串行化. 
- 优先图转为串行化方案: 必须保持原有的方向性, 没有箭头的可以调换顺序
- 锁: 使用二阶段锁, 如果有写, 要用exclusive lock, 如果只有读, 只用shared lock就行. shared lock可以由多个事务持有, 但是exclusive lock在某个时刻只能由一个事务持有. 分为两个阶段, growing phase和shrinking phase, 前者只获得锁不释放锁; 后者只释放锁不获得锁
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
5. 若为冲突可串行化, 根据precedence graph, 可以调换两者之间不存在箭头的事务的顺序, 得到数个串行化调度

## 存储与索引

要点:

- 阻塞因子: 块大小/记录大小, 若<1, 则发生"记录跨块"
- LRU和MRU算法: LRU, 替换掉最久未使用的数据块; MRU, 替换掉最近使用的数据块
- 文件和页面: 一张表对应一个文件, 一个文件对应数个页面, 一个页面对应一个或多个块. 若一个页面为4k, 页头固定250字节元数据, occupancy为80%, 则每页有(4k-250)*0.8=3076字节来存储数据, 设每个记录的大小为200字节, 则向下取整后可以存储15条数据. 假设该文件有2000000条记录, 则总共需要的页数为2000000/15向上取整为133334页. 实际占用空间为4k\*133334=546136064字节, overhead为(546136064-400000000)/400000000=36.53%
- 三种文件组织: 无序文件, 排序文件, 索引文件
- 访问路径: 线性扫描(很慢, 基本要扫描一半的页), 二分扫描(维护成本很高), 索引扫描
- B+树: 假设表存储在140351个页面的文件中, 页面按照逻辑排序(物理上不一定连续), 索引条目由搜索键和行指针构成, 共8字节. 假设每页的总可用空间为3846字节, 填充因子为75%, 则向下取整后可以存放360条索引. 最底层索引总共需要140351个, 所以需要的索引页数向上取整后为390页. 对于这个390页索引页, 在它的基础上继续套娃建立索引, 那么需要390/360向上取整2页来存放, 继续套娃, 最顶层只需要1页. 所以索引页的总数为393. 相对于140351个数据页, 仅仅增加了0.2%的需求. 在查询的时候, 只需要存放3个索引页和1个数据页入内存, 也就是4次IO. B+树的最底层是数据页.
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

- 嵌套循环连接: b_R+|R|*b_S, R是外表, |R|是R元组的数量, b是block数量
- 块嵌套循环连接: b_R+b_R*b_S, R是外表, b是block数量
- 索引嵌套循环连接: b_R+|R|*c, R是外表, c是对S表索引的平均成本
- 外部合并排序: 建议考试前复习一下PPT上的那个例子
- 评估策略: Materialization和Pipelining, 前者把中间结果存储到一个临时关系中, 供后续使用, 后者是直接将输出传递给下一个操作

相关知识点:

- [nested loop join](/database/query-processing/#nested-loop-join)
- [block nested loop join](/database/query-processing/#block-nested-loop-join)
- [index nested loop join](/database/query-processing/#index-nested-loop-join)

## ED Revision参考

- Q2
	- ABCDEFGHIJ
	- Since both A and I are not superkey and AI is a superkey, AI is a candidate key
	- HI, AI
	- ABCDEFGH
	- B is not a prime key, since it's not part of any candidate key (HI, AI)
	- Not examinable
	- The intersection of these three relations is none, and none is not the key of any relations
	- 3NF, non-prime attribute can not depends on non-prime attribute, so B -> D violates 3NF
	- Not examinable 
	- BCNF, LHS must be superkey, A -> B, A is not a superkey (you can verify it using attribute closure), so it violates BCNF
- Q4
	- T1, r(x_1), w(x_1); T2, r(x_1), w(x_1); There are two possible anomalies, lost update, T2 reads x_1 before T1 writes to x_1; temporary read, T2 reads x_1 but T1 rollbacks later. the correct result is \$1500, the result of lost update is \$2500, the result of temporary update is \$2000, suppose the initial fund is \$2000
    - T1, r(x_1), w(x_1); T3, r(x_1), w(x_1), r(x_2), w(x_2), lost update, T3 read x_1 before T1 write to x_1. The amount of 201 would be \$1700 which is incorrect. We can use the exclusive lock, T1 first gets the lock, T3 keeps waiting until T1 releases the lock
	- Dirty reads == temporary reads, the other two are not examinable. The isolation level is serializable. 
	- Deak lock occurs when two resources waiting for each other to release their locks. Possible scenario: T1 gets lock on 201, T3 gets lock on 203. Suppose T1 needs to update some status of 203, T1 needs lock of 203, T3 needs lock of 201, it's a deadlock
	- Share lock can be held by multiple transactions at the same time while exclusive lock is not. We can attach exclusive lock on T1 and T2 to prevent anomalies, because they need to write on the same data, which will potentially cause lost update or temporary read
	- COMMIT is used to commit a transaction, ROLLBACK is used to undo the transaction, revert back to the original state. It will lead to temporary read.
	- 2PL: 2 phase locking, as its name suggests, has two phases, growing phase and shrinking phase, during growing phase, a transaction does not release any locks but acquire locks; during shrinking phase,  a transaction does not acquire any locks but release locks. This will ensure transaction always be executed after other transactions release the desired lock
	- Not examinable
	- Not examinable 
	- T1, r(x_1), w(x_1); T3, r(x_1), w(x_1), r(x_2), w(x_2). There are three conflicts here: T1 r(x_1) and T3 w(x_1); T1 w(x_1) and T3 r(x_1). T1 w(x_1) and T3 w(x_1). There exists a circle in the precedence graph, so it's not conflict serializable.
- Q5

	The storage can be used in a page: (8192-300)\*0.9=7102.8 bytes. The table needs 2000000\*(4+10+6+15+4)=78000000 bytes. 78000000/7102.8=10981.58, so we need 10982 pages to store the entire inventory table, the total space needed 10982\*8192=89964544 bytes, overhead is (89964544-78000000)/78000000=15.33%. The time for loading each page is 200 milliseconds, so we need 200*10982=2196400 milliseconds to scan the entire table. The search key takes (10+4) bytes, so the index entry takes 14+4=18 bytes, we can store 7102.8/18=394.6 which is 394 records in one page, so we need 2000000/394=5076.14 which is 5077 pages to store all the indices. We need 5077/394=12.89 which is 13 pages to store the bottom index pages, we need 1 page at root level. So the B+ tree looks like this: 1 page at top, 13 pages in between, 5077 pages at the bottom and there are 10982 leaf nodes. For a single query, we need 4 IOs(let's assume that one page = one IO, which is default in this course), so it takes 4\*200=800 milliseconds to reach the specific leaf nodes. 

## Practice Final Exam

- 7

	- 

		```sql
		SELECT branch_name 
  		FROM branch 
  		WHERE assets >= SOME (
  			SELECT assets FROM branch WHERE branch_city = 'Gold Coast'
  		);
  		```

	- 

		```sql
		SELECT depositor.customer_name, AVG(account.balance)
		FROM account
		JOIN depositor ON account.account_number = depositor.account_number
		WHERE depositor.customer_name IN (
			SELECT customer.customer_name
			FROM customer
			JOIN depositor ON customer.customer_name = depositor.customer_name
			WHERE customer.customer_street = 'Johnson'
			GROUP BY customer.customer_name
			HAVING COUNT(depositor.account_number) >= 3
		)
		GROUP BY depositor.customer_name;
		```
  
    - 

		```sql
		SELECT depositor.customer_name
  		FROM depositor 
  		JOIN borrower ON borrower.customer_name = depositor.customer_name 
  		WHERE borrower.loan_number IN (
  			SELECT loan_number FROM loan WHERE branch_name = 'Darling Harbour'
  		);
		```

- 8

	Let's assume that:

	- Cursor_no: A
	- Sec_no: B
	- Offering_dept: C
	- Credit_hours: D
	- Course_level: E
	- Instructor_id: F
	- Semester: G
	- Year: H
	- Days_hours: I
	- Room_no: J
	- No_of_students: K

	we have the following functional dependencies: 
	
	- A -> CDE
	- ABGH -> IJKF
	- JIGH -> FAB

	a) Let's verify if JIGH is a candidate key. (JIGH)+=FABCDEJIGH=FABCDEJIGHK=R, so it's a super key. Obviously, J, I, G, H, JI, JG, JH, IG, IH, GH is not a super key, so JIGH is a candidate key. Let's verify if ABGH is a candidate key. (ABGH)+=ABCDEHIJKFG=R, so it's a superkey. Obviously, A, B, G, H, AB, AG, AH, BG, BH, GH is not a super key, so ABGH is a candidate key.

	b) R is not in BCNF because in FD A -> CDE, A is not a super key. So we can decompose it into R1(A, C, D, E) and R2(A, B, G, H, J, I, F). It's a lossless decomposition because the intersection of R1 and R2 A is a candidate key of R1. Also, It preserves the FDs. Since we have A -> CDE in R1 and ABGH -> IJKF, JIGH -> FAB in R2.

- 9

	- The equivalent SQL command for this is `SELECT customer_name FROM customer WHERE customer_city = 'Sydney'`, it can be converted to relational algebra as follows: π~customer_name~(σ~customer_city='Sydney'~(customer))
	- The equivalent SQL command for this is `SELECT borrower.customer_name FROM borrower JOIN loan ON borrower.loan_number = loan.loan_number WHERE loan.branch_name = 'Redfern' AND customer_name NOT IN (SELECT customer_name FROM depositor)`, it can be converted to relational algebra as follows: π~customer_name~(σ~branch_name='Redfern'~(borrower⋈~loan_number~loan))-π~customer_name~(depositor)

- 10

	- There are 5 conflicts in this case. R3 -> W1, W1 -> R2, R1 -> W3, R2 -> W3, W1 -> W3, so we have 3 -> 1, 1 -> 2, 1 -> 3, 2 -> 3, note that we have 3 -> 1 and 1 -> 3, so it's not conflict serializable
	- There are 2 conflicts in this case. R1 -> W3, W3 -> R2, R3 -> W1, W1 -> R2, so we have 1 -> 3, 3 -> 2, 3 -> 1, 1 -> 2, note that we have 1 -> 3 and 3 -> 1, so it's not conflict serializable

- 11

	**Let's assume that Employee is the outer table**

	- Nested Loop Join: b_R+(|R|\*b_S), so it's 200+(2000\*500)=1000200 times IO
	- Block-nested loop Join: b_R+(b_R\*b_S), so it's 200+(200\*500)=100200 times IO
	- Index-nested loop join: let's assume that the average cost of indexing is 3 times. b_R+(|R|\times c), so it's 200+(2000\*3)=6200 times IO

	Same for Department as outer table