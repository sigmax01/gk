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

        上述给定查询的关系表达式为: π Branchname,Assets (σ Customercity='Sydney'(Customer⋈Deposit⋈Branch)). 上述三个表的自然连接可能产生一个非常大的关系, 无法放到内存中. 在这里, 我们其实只需要一些有用的`Cusomtercity`为`Sydney`的起始元组, 并且, 查询的最终需求是`Branchname`和`Assets`, 这意味着早较早阶段就应该丢弃其他不需要的字段. 

        如上述的表达式可以修改为π Branchname,Assets ((π customername (σ Customercity='Sydney' (Customer)))⋈Deposit⋈π branchname,assets (Branch)). 首先从`Customer`表中筛选出`CustomerCity='Sydney'`的记录, 然后只丢弃不需要的`street`和`customercity`字段. 

    === "例子2"

        考虑以下的查询: "找到在悉尼有客户存款找过$500的银行的资产和名称". 