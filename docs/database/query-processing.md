---
title: 数据库:查询处理
comments: true
---

## 查询处理流程

查询处理流程可以简单的分为:

1. 语义检查和查询重写: 检查查询语句是否有语法错误或者语义问题. 然后将SQL查询转换为[关系代数表达式](/database/relational-algebra), 可以被表示为一颗表达式树(expression tree), 如[图](https://img.ricolxwz.io/a99283244cfa79f7c7629924cc0cff5d.png)所示. 最后将[视图](/database/advanced-sql/#view)替换为实际的子查询, 以便进一步处理
2. 查询优化: 在所有等价的查询计划中, 选择成本最低的计划:
    1. 逻辑查询计划优化: 在关系代数层面使用启发式方法(对表达式树进行重新排列操作, 以减少中间结果的大小, 减少临时数据的存储和计算量)进行优化
    2. 物理查询计划优化: 基于成本估算(最小化磁盘IO次数)选择合适的查询执行策略
3. 执行查询: 根据最优查询执行策略执行

## 查询优化

### 逻辑查询计划优化

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

#### 等价代数表达式转化规则

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

### 物理查询计划优化

物理查询计划读取上一步产生的逻辑查询计划树然后产生一个查询计划. 该计划会为逻辑查询计划中的每一个操作符选择一个算法. 最终, 在所有等价的查询计划中找到一个最优计划, 选择IO次数最少的物理查询计划. 如[图](https://img.ricolxwz.io/1d09130ce83e4a5cd350b1e3a7a973ac.png), 会产生一些不同的物理查询计划树.

与逻辑查询计划树类似, 一个带有物理操作符的查询计划树称为物理查询计划, 如[图](https://img.ricolxwz.io/9dc039f22f74584a5dffeb865e233b5d.png)o

#### 计算成本

可以通过以下信息计算一个物理查询计划的成本: 

- 访问方法: 使用不同的[访问方法](/database/storage-indexing/#access-path)会影响IO成本
- 物理组织: 包括数据的物理存储结构, 例如blocking factor, stored table?
- 统计信息: 表示满足选择条件的数据量

通过对成本的估计和优化, 输出一个高效的物理查询计划.

#### 优化连接操作

在SQL查询中, 连接操作是最常见的, 同时也是执行成本最高的操作, 因为连接操作会涉及大量的IO. 因此, 优化连接操作对于提高查询性能至关重要.

如考虑以下的SQL查询: `SELECT * FROM Student R, Enrolled S WHERE R.sid=S.sid`, 笛卡尔积R×S后面接上一个选择操作在语义上等于自然连接, 即R⋈S, 但是R×S这个产生的中间结果往往很大. 因此, 执行笛卡尔积后再选择是不高效的, 应当使用等价的优化连接操作来替代.

几种常见的实现算法有:

- 嵌套循环连接: Nested Loop Join
- 块嵌套循环连接: Block-nested loop join
- 索引嵌套循环连接: Index-nested loop join

根据IO来选择合适的实现算法.

???+ example "例子"

    假设:

    - `Student`: 包括了学生的基本信息, `sid`, `name`, `gender`, `country`
    - `Enrolled`: 包括了学生的选课记录, `sid`, `uos_code`, `semester`

    - `|R|`: 表示关系`R`中元组的数量, 这里假设`|R|=1000`
    - `|S|`: 表示关系`|S|`中的元组数量, 这里假设`|S|=1000`

    - `b_R`: 表示`Student`表的页数, 这里假设`b_R=100`
    - `b_S`: 表示`Enrolled`表的页数, 这里假设`b_S=400`

    我们要执行的操作是Student⨝Enrolled. 也就是基于`sid`对两个表进行连接.

##### 嵌套循环连接

循环嵌套连接可以用伪代码表示为:

```
for each page BR of R do
    for each tuple r in BR do
        for each page BS of S do
            for each tuple s in BS do
                if θ(r,s)=true then add <r,s> to the result
```

即, 对于R中的每一个元组, 我们要扫描整一个S表. 这样做的好处是不需要任何索引, 可以被用于任何形式的条件连接. 缺点就是非常的消耗计算资源.

- 来自于`R`的IO: 读取`b_R`个表到内存
- 来自于`S`的IO: 对于每一个`R`中的元组, 都要读取`S`的所有表, 所以是`|R|*b_S`

所以, 总的消耗是`b_R+|R|*b_S`.

???+ example "例子"

    上述的例子中, 如果`Student`位于外层, 则复杂度为100+1000\*400=400100次IO. 如果`Enrolled`位于外层, 则复杂度为400+10000\*100h=10004000次IO. 

##### 块嵌套循环连接

块嵌套循环连接可以用伪代码表示为:

```
for each page BR of R do
    for each page BS of S do
        for each tuple r in BR do
            for each tuple s in BS do
                if θ(r,s)=true then add <r,s> to the result
``` 

可以看到, 只是两条语句对换了一下位置. 对于每一个R页面, 遍历S中的每一个页面, 在内存中读取R中每一个元组, 和S中的每一个元组匹配. 

- 来自于`R`的IO: `b_R`, 即`R`表的每个页面只需要读取一次
- 来自于`S`的IO: `b_R*b_S`, 因为每个`R`的页面都要读取`S`的所有页面

所以总的IO成本是: `b_R+b_R*b_S`.

???+ example "例子"

    上述的例子中, 如果`Student`位于外层, 则复杂度为100+100\*400=40100次IO. 如果`Enrolled`位于外层, 则复杂度为400+400\*100=40400次IO.

##### 索引嵌套循环连接

索引嵌套循环连接可以用伪代码表示为:

```
for each page BR of R do
    for each tuple r in BR do
        for each tuple s in idx(r) do
            add <r,s> to result
```

要使用索引嵌套循环嵌套连接, 必须满足以下条件:

- 连接必须是等值连接或者自然连接
- 内表的连接属性上有索引

假设S表的连接属性, 如`sid`有索引`idx(sid)`. 对于R表的每个页面, 对于页面的每个元组, 使用索引`idx(sid)`查找满足连接条件的元组, 加入结果. 

- 来自于`R`的IO: `b_R`
- 来自于`S`的IO: `|R|*c`, `c`是对`S`表的索引进行遍历和查找的平均成本(包含索引访问和匹配元组读取)

???+ example "例子"

    - `c_1=4`表示对`S`使用索引查找的平均成本
    - `c_2=3`表示对`R`使用索引查找的平均成本

    上述的例子中, 如果`S`表有索引的时候, 则复杂度为100+1000\*4=4400次IO. 如果`R`表有索引的时候, 则复杂度为400+10000\*3=30400次IO.

通常情况下, 我们会选择元组较少的表作为外表, 这样可以减少索引查找的次数, 进而降低IO成本. 在本例中, 使用`S`表的索引会比使用`R`表的效率更高, 因为`R`表较小, 查找次数少.

#### 优化排序操作

在SQL查询中, 可以通过`ORDER BY`关键字得到经过排序的输出. 一些SQL操作如`JOIN`, `GROUP BY`, `DISTINCT`, `UNION`, `DIFFERENCE`等在输入是排序的情况下执行效率更高. 

???+ example "例子"

    例如, 投影操作, 考虑以下的SQL操作`SELECT DISTINCT sid, bid FROM Reserves`. 在默认情况下, 为了确保返回的结果中每个`sid, bid`组合都是唯一的, 如果文件未排序, 则去重操作可能需要将每个记录与文件中的所有其他值逐一比较, 从而增加了时间和资源消耗o

Sort-Merge Join是实现连接操作的又一种方法, 在进行连接操作的时候, 将两张表按照连接属性排序, 然后通过线性扫描匹配对应的值. 在这种Join算法中, 最昂贵的部分是对输入的两张表进行排序. 

对于小的, 能够装入内存的表, 可以使用QuickSort等排序算法, 这种算法在内存中排序时效率较高. 但是对于大型数据库, 这种方法不可行. 例如, 在4GB内存中对10GB的数据无法进行排序. 这个使用, 我们通常采用的是External Merge-Sort算法, 即外部合并排序.

##### 外部合并排序

用B表示内存的大小, 用N表示文件的大小(单位都是页), 外部合并排序主要分为三步:

1. 创造排序的runs(run是一小部分排序好的记录)

    1. 从磁盘中读取B页记录到内存中
    2. 对内存中的页进行排序
    3. 将排序好的数据写回到磁盘中

    总共这样读取-写回的次数是m=$\lceil N/B\rceil$

2. 进行(B-1)路合并

    使用B-1页内存来缓冲run, 并使用剩余的1页内存作为输出缓冲区, 读取每个Run的第一个页到分配的输入缓冲区中

    1. 从所有输入缓冲页中选择第一个最小的记录
    2. 将选取的记录写入输出缓冲区中, 如果输出缓冲区已满, 则写回到磁盘中
    3. 如果对于某个Run来讲是**在当前页中后一最后一条放入输入缓冲区的记录, 则从该Run的下一页读取数据到输入缓冲区中; 如果当前Run中已经没有更多的页了, 那么继续下一个Run

    直到所有的输入缓冲区为空. 例子请见课件.

3. 每次合并后, 数量减少到原来的(B-1)分之一. 如果$m\geq B$, 则说明需要多次合并. 合并的次数公式为$\lceil \log_{(B-1)}(N/B)\rceil+1$(包括初始的排序)

## 评估策略

两种数据库操作评估的策略:

- 物化: Materialization, 也称为"set-at-a-time"方式, 在这种策略下, 数据库会一次完成一个操作, 并将操作结果存储到一个临时关系中, 供后续操作使用, 每个操作的输出都会被写入磁盘, 接下来的操作会从磁盘中读取这些数据, 这种方式的优势在于操作的独立性, 每个操作完成之后都有中间存储, 但是缺点是频繁的读写, 性能可能较低
- 管道化: Pipelining, 也称为"tuple-at-a-time"方式, 在这种策略下, 数据库会将多个操作放在一个流水线中处理, 即每个操作的输出直接传递给下一个操作, 无需写入磁盘, 这种方式减少了IO的开销, 因为数据直接在内存中传递, 但是, 这种操作需要更多的内存兼容性, 即每个操作必须能够接受前一个操作的输出格式