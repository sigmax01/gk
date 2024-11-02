---
title: 数据库:查询处理
comments: false
---

## 查询处理流程

查询处理流程可以简单的分为:

1. 语义检查和查询重写: 检查查询语句是否有语法错误或者语义问题. 然后将SQL查询转换为[关系代数表达式](/database/relational-algebra), 可以被表示为一颗表达式树(expression tree), 如[图](https://img.ricolxwz.io/a99283244cfa79f7c7629924cc0cff5d.png)所示. 最后将[视图](/database/advanced-sql/#view)替换为实际的子查询, 以便进一步处理
2. 查询优化: 在所有等价的查询计划中, 选择成本最低的计划:
    1. 逻辑查询计划优化: 在关系代数层面使用启发式方法(对表达式树进行重新排列操作, 以减少中间结果的大小, 减少临时数据的存储和计算量)进行优化
    2. 物理查询计划优化: 基于成本估算(最小化磁盘IO次数)选择合适的查询执行策略
3. 执行查询: 根据最优查询执行策略执行

### 查询优化

#### 逻辑查询计划优化

我们可以将任何元组演算表达式(如SQL)转换为等价的代数表达式. 在转换为代数表达式的过程中, 需要进行启发式优化, 这个优化通常聚焦于一元操作(如选择, 投影), 因为这些操作往往可以在早期阶段就过滤掉大量数据, 使得每一步的中间结果尽量小, 中间结果小, IO操作就越少, 从而提高执行效率.

???+ example "例子"

    === "例子1"

        例如考虑以下的查询: "找到在悉尼有客户存款的银行的资产和名称". 数据库中包含三个表, 分别是`Deposit`, `Customer`, `Branch`, 每个表的结构如下:

        - `Deposit`: 包含`branchname`, `account#`, `customername`和`balance`
        - `Customer`: 包含`customername`, `street`和`customercity`
        - `Branch`: 包含`branchname`, `assets`, `branchcity`

        上述给定查询的关系表达式为: π~Branchname,Assets~(σ~Customercity=Sydney~(Customer⋈Deposit⋈Branch)). 上述三个表的自然连接可能产生一个非常大的关系, 无法放到内存中. 在这里, 我们其实只需要一些有用的`Cusomtercity`为`Sydney`的起始元组.

        如上述的表达式可以修改为π~Branchname,Assets~((σ~Customercity=Sydney~(Customer))⋈Deposit⋈Branch).

        此外, 应该尽早丢弃不必要的属性, 即尽早执行投影. 一个启发是我们应该移除掉所有的不在剩余操作中起作用的属性. 

        如上面的表达式中, σ~Customercity=Sydney~(Customer)⋈Deposit这个操作产生的属性中, 只有`branchname`是有用的属性, 所以应该提前进行投影, 修改后的代数表达式是Π~Branchname,Assets~(Π~Branchname~(σ~Customercity=Sydney~(Customer)⋈Deposit)⋈Branch)

        我们能做得更好吗? 😅 可以的! 注意到, 在连接`Branch`表的时候, `branchcity`这个属性是不用的, 我们要把它提前移除, 修改之后的表达式是Π~Branchname~(σ~Customercity=Sydney~(Customer)⋈Deposit)⋈Π~Branchname,Assets~(Branch)

    === "例子2"

        - `Deposit`: 包含`branchname`, `account#`, `customername`和`balance`
        - `Customer`: 包含`customername`, `street`和`customercity`
        - `Branch`: 包含`branchname`, `assets`, `branchcity`

		考虑以下的查询: "找到在悉尼有客户存款找过$500的银行的资产和名称". 对于这个查询, 最初给出的表达式是Π~Branchname,Assets~ (σ~Customercity=Sydney∧Balance>500~(Customer⋈Deposit⋈Branch)). 注意, 我们无法仅对`Customer`表进行筛选操作, 因为`Balance`是`Deposit`表的属性. 

        需要在`Customer`表和`Deposit`表进行连接之后, 再进行选择操作. 因此, 正确的表达式应该是: Π~Branchname,Assets~(σ~Customercity=Sydney∧Balance>500~((Customer⋈Deposit)⋈Branch)).
        
        我们可以做得更好吗? 答案是肯定的. 

        首先, 我们能把选择语句拆分成两个部分: Π~Branchname,Assets~(σ~Customercity=Sydney~(σ~Balance>500~(Customer⋈Deposit))⋈Branch)

        然后, 可以在连接之前先应用筛选条件: Π~Branchname,Assets~(σ~Customercity=Sydney~(Customer)⋈σ~Balance>500~(Deposit)⋈Branch)

        这样能够进一步减少中间的数据规模. 

##### 等价代数表达式转化规则

- 交换律: R1⋈R2=R2⋈R1
- 结合律: (R1⋈R2)⋈R3=R1⋈(R2⋈R3)
- 投影的级联: 如果B1, ..., Bn是A1, ..., An的子集, 那么Π~B1,...,Bn~(Π~A1,...,An~(R))=Π~B1,...,Bn~(R)
- 选择的级联: σ~θ1~(σ~θ2~(R))=σ~θ2~(σ~θ1~(R))=σ~θ1∧θ2~(R)
- 选择对连接的分配性: σ~θ~(R1⋈R2)=(σ~θ~(R1))⋈R2, 当θ只涉及R1的属性时

???+ example "例子"

    考虑如下的关系: 

    - `Deposit`: 包含`branchname`, `account#`, `customername`和`balance`
    - `Customer`: 包含`customername`, `street`和`customercity`
    - `Branch`: 包含`branchname`, `assets`, `branchcity `

    考虑以下的查询: "找到在悉尼有客户存款找过$500的银行的资产和名称". 对于这个查询, 最初给出的表达式是Π~Branchname,Assets~ (σ~Customercity=Sydney∧Balance>500~(Customer⋈Deposit⋈Branch)). 注意, 我们无法仅对`Customer`表进行筛选操作, 因为`Balance`是`Deposit`表的属性. 

    根据选择对连接的分配性, 有Π~Branchname,Assets~(σ~Customercity=Sydney∧Balance>500~((Customer⋈Deposit)⋈Branch)).

    根据选择的级联, 有Π~Branchname,Assets~(σ~Customercity=Sydney~(σ~Balance>500~(Customer⋈Deposit))⋈Branch)

    使用两次选择对连接的分配性, 有Π~Branchname,Assets~(σ~Customercity=Sydney~(Customer)⋈σ~Balance>500~(Deposit)⋈Branch)

#### 物理查询计划优化

物理查询计划读取上一步产生的逻辑查询计划树然后产生一个查询计划. 该计划会为逻辑查询计划中的每一个操作符选择一个算法. 最终, 在所有等价的查询计划中找到一个最优计划, 选择IO次数最少的物理查询计划. 如[图](https://img.ricolxwz.io/1d09130ce83e4a5cd350b1e3a7a973ac.png), 会产生一些不同的物理查询计划树.

与逻辑查询计划树类似, 一个带有物理操作符的查询计划树称为物理查询计划, 如[图](https://img.ricolxwz.io/9dc039f22f74584a5dffeb865e233b5d.png)o

##### 计算成本

可以通过以下信息计算一个物理查询计划的成本: 

- 访问方法: 使用不同的[访问方法](/database/storage-indexing/#access-path)会影响IO成本
- 物理组织: 包括数据的物理存储结构, 例如blocking factor, stored table?
- 统计信息: 表示满足选择条件的数据量

通过对成本的估计和优化, 输出一个高效的物理查询计划.

##### 优化连接操作

在SQL查询中, 连接操作是最常见的, 同时也是执行成本最高的操作, 因为连接操作会涉及大量的IO. 因此, 优化连接操作对于提高查询性能至关重要.

如考虑以下的SQL查询: `SELECT * FROM Student R, Enrolled S WHERE R.sid=S.sid`, 笛卡尔积R×S后面接上一个选择操作在语义上等于自然连接, 即R⋈S, 但是R×S这个产生的中间结果往往很大. 因此, 执行笛卡尔积后再选择是不高效的, 应当使用等价的优化连接操作来替代.

几种常见的实现算法有:

- 嵌套循环连接: Nested Loop Join
- 块嵌套循环连接: Block-nested loop join
- 索引嵌套循环连接: Index-nested loop join

根据IO来选择合适的实现算法.