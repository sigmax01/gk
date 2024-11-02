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

