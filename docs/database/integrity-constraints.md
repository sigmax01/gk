---
title: 数据库:完整性约束
comments: true
---

## 概念

完整性约束是数据库中的每一个实例都符合的一个条件. 又可以被称为ICs, Integrity Constraints. ICs是在数据库最初设计的时候就需要考虑并定义的内容, 可以通过`CREATE TABLE`的命令实现. 也可以在任意时间通过`ALTER TABLE <table_name> ADD/ALTER <constraints>`来添加或更新ICs. 

???+ warning "注意"

    在执行完整性约束修改/添加命令的时候, 数据库会先确保关系满足指定的约束:
    
    - 如果满足, 约束将添加到关系中
    - 如果不满足, 命令会被拒绝

一个合法的关系实例是满足所有指定ICs的关系实例, 但是并不是所有的时候都满足, 可以存在暂时不满足的情况. 如在同一个事务中先插入一个新的订单, 然后再插入对应的客户信息时, 可能会出现一种暂定的状态: 订单记录已经插入, 但是对应的客户记录还没有插入, 这时候客户记录可能不满足完整性约束.

## 数据库中的ICs

在数据库中, ICs在数据库结构设计阶段就被声明了. 数据库的设计者应该确保ICs之前互相不抵触, 这可以通过技术实现自动化检测, 但是开销太大. 数据库会在某一部分发生改变的时候进行ICs检测. 我们也可以声明ICs检测的时间, 如在紧贴着一条SQL语句或者在某个事务结束的时候. 如果违法了ICs, 可能的响应方式有:

- 拒绝当前数据库操作, 不执行
- 中止整一个事务, 回滚所有在同一个事务中已经执行的操作 
- 执行一系列维护指令

## 事务

事务就是一组被作为整体执行的SQL语句, 这个操作具有原子性. 其语法为:

```sql
BEGIN;
    <statement1>;
    <statement2>;
    <statement3>;
COMMIT;
```

## 类型

- 静态ICs

    静态ICs描述了数据库中的每一个合法实例都必须满足的条件. 这意味着静态完整性约束是状态无关的. 当插入, 删除或者更新操作违反了这些约束的时候, 这些操作会被禁止. 静态ICs有四种类型: [域约束(Domain Constraints)](#域约束), [键约束](#键约束)及[参照完整性约束(Key Constraints & Referential Integrity)](#参与完整性约束), [语义完整性约束(Semantic Integrity Constraints)](#语义完整性约束), 断言(Assertions).

- 动态ICs

    这些约束是基于数据库状态变化的谓词, 捕获两个或多个状态之间的条件. 因此, 动态ICs是状态相关的, 例如触发器, 它们会在数据库状态发生变化的时候执行特定的操作.

## 静态ICs

### 域约束 {#域约束}

数据库中的每一个字段都应该具有合适的数据类型. 每当向数据库中插入数据的时候, 系统会检查数据是否符合该字段定义的数据类型, 这种检查是自动进行的, 确保不符合的数据无法插入. 在执行查询的时候, 数据库系统会检查各个字段之间的值的比较是否有意义, 例如, 防止在比较字符串和数字的时候出现错误. 

SQL的DDL语句允许字段在`CREATE TABLE`语句中被进一步约束: 

- `DEFAULT`: 若在`INSERT`语句中值被省略的话字段的默认值
- `NOT NULL`: 字段值不允许为`NULL`
- `NULL`: 字段的值可以是`NULL`, 默认情况

???+ example "例子"

    ```sql
    CREATE TABLE Student
    (
        sid INTEGER NOT NULL,
        name VARCHAR(20) NOT NULL,
        semester INTEGER DEFAULT 1,
        birthday DATE NULL,
        country VARCHAR(20)
    )
    ```

除了数据类型约束以外, 还可以使用`CHECK`语句对字段的取值范围进行约束. 

???+ example "例子"

    ```sql
    CREATE TABLE Student
    (
        sid INTEGER NOT NULL,
        name VARCHAR(20) NOT NULL,
        semester INTEGER DEFAULT 1,
        birthday DATE NULL,
        country VARCHAR(20),
        grade CHAR(1) CHECK(grade IN ('F', 'P', 'C', 'D', 'H')),
        age INTERGER CHECK(age >= 0)
    )
    ```

#### 自定义域

自定义域是为某个字段自定义的数据类型, 取值范围等于约束的总和. 

???+ example "例子"

    先来看没有自定义域下的写法:

    ```sql
    CREATE TABLE Student (
        sid INTEGER NOT NULL,
        name VARCHAR(20) NOT NULL,
        grade CHAR (1) DEFAULT ’P’ CHECK (grade IN (‘F’,’P’,’C’,’D’,’H’)),
        birthday DATE );
    ```

    自定义域`Grade`: `CREATE DOMAIN Grade CHAR(1) DEFAULT ’P’ CHECK(VALUE IN (‘F’,’P’,’C’,’D’,’H’))`, 然后可以在创建表的时候这么写:

    ```sql
    CREATE TABLE Student (
        sid INTEGER NOT NULL,
        name VARCHAR(20) NOT NULL,
        grade Grade,
        birthday DATE );
    ```

### 键约束 {#键约束}

在SQL中, 我们使用`PRIMARY KEY`和`UNIQUE`语句处理键约束, 主键默认为`UNIQUE`和`NOT NULL`. 一个表中可以有多个候选键(可以使用`UNIQUE`定义), 但是只能有一个主键. 若主键由多个字段构成, 则需要按照下述方式声明主键:

???+ example "例子"

    ```
    CREATE TABLE Boat
    (
        name VARCHAR(20),
        colour VARCHAR(20),
        PRIMARY KEY (name, colour)
    );
    ```

### 参与完整性约束 {#参与完整性约束}

参与完整性约束确保在数据库中, 表与表之间通过外键建立的引用关系始终保持一致. 对于每一个子表/从属表中的一个元组的外键为$\alpha$, 则一定有一个父表/被引用表的元组其被引用的属性的值为$\alpha$. 

可以简单的理解为外键不能出现悬空引用, 如[图](https://img.ricolxwz.io/e0fa20affecb5a6d2c2498656ef05f81.png). 理解外键不能出现悬空之后, 就可以很好的理解外键约束在父表上执行删除或更新操作时的几种选项:

1. 默认选项(`NO ACTION`): 当在父记录上执行删除或者更新操作的时候, 默认情况下不采取任何动作. 这意味着, 如果试图删除或者更新一个在外键中被引用的父记录, 数据库将拒绝执行该动作, 防止破坏参照完整性
2. 级联操作(`CASCADE`): 当在父记录上执行删除或者更新操作的时候, 所有引用该记录的子记录也会相应地被删除或者更新. 这种操作确保所有引用的记录保持一致性
3. 设置为`NULL`或者默认值(`SET NULL`/`SET DEFAULT`): 当在父记录上执行删除或者更新操作的时候, 所有引用该父记录的子记录中的外键将被设置为`NULL`或者预设的默认值. 这在某些情况下可以避免删除子记录, 只是将其和父记录的关联解除

???+ example "例子"

    ```sql
    CREATE TABLE Enrolled
    (
        -- the sid field default value is 12345
        sid CHAR(5) DEFAULT 12345,
        uos CHAR(8),
        grade VARCHAR(2),
        PRIMARY KEY (sid,uos),
        FOREIGN KEY (sid) REFERENCES Student
        -- the on delete cascade conveys that an enrolled row should be deleted when the student with sid that it refers to is deleted
        ON DELETE CASCADE
        -- the on update set default will update the value of sid to a default value that is specified as the default in this enrolled schema definition
        ON UPDATE SET DEFAULT
    );
    ```

### 语义完整性约束 {#语义完整性约束}

语义完整性约束, Semantic Integrity Constraints, 乍一看和前面所说的[域约束](#域约束)好像差不多, 实际上是有区别的, 域检查约束专注于单个属性的数据有效性, 确保其符合数据类型, 取值范围或者格式等基本要求, 语义完整性约束涉及到更加复杂的业务逻辑和数据关系, 确保数据在语义层面上符合业务规则.

???+ example "例子"

    ```sql
    CREATE TABLE Assessment
    (
        sid INTEGER REFERENCES Student,
        uos VARCHAR(8) REFERENCES UnitOfStudy,
        mark INTEGER,
        CHECK (mark BETWEEN 0 AND 100)
    );
    ```

### 技巧

#### 自定义约束名称

可以使用`CONSTRAINT`为域约束, 参与完整性约束, 语义完整性约束等等套一层名称的皮. 

???+ example "例子"

    ```sql
    CREATE TABLE Enrolled
    (
        sid INTEGER,
        uos VARCHAR(8),
        grade VARCHAR(2),
        CONSTRAINT FK_sid_enrolled FOREIGN KEY (sid)
        REFERENCES Student
        ON DELETE CASCADE,
        CONSTRAINT FK_cid_enrolled FOREIGN KEY (uos)
        REFERENCES UnitOfStudy
        ON DELETE CASCADE,
        CONSTRAINT CK_grade_enrolled CHECK(grade IN (‘F’,...)),
        CONSTRAINT PK_enrolled PRIMARY KEY (sid,uos)
    );
    ```

#### 约束检查的时间 {#约束检查的时间}

默认情况下, 所有的约束都会在元组出现变更之后立即进行检查, 对应的参数为`NO DEFERABLE`. 然而, 可以通过设置参数为`DEFERRABLE`知道事务(transaction)结束之后再检查, 这个参数下面又细分为两种:

- `INITIALLY DEFERRED`: 默认直到事务完成之后再检查, 然而, 可以通过设置参数`SET CONSTRAINTS <name> IMMEDIATE`动态修改为立即检查
- `INITIALLY IMMEDIATE`: 默认立即检查, 然而, 可以通过设置参数`SET CONSTRAINTS <name> DEFERRED`动态修改为直到事务完成之后再检查

???+ example "例子"

    ```sql
    CREATE TABLE UnitOfStudy
    (
        uos_code VARCHAR(8),
        title VARCHAR(20),
        lecturer_id INTEGER,
        credit_points INTEGER,
        CONSTRAINT UoS_PK PRIMARY KEY (uos_code),
        CONSTRAINT UoS_FK FOREIGN KEY (lecturer_id)
        REFERENCES Lecturer DEFERRABLE INITIALLY DEFERRED
    );
    ```

    这允许我们插入一UnitOfStudy记录, 在插入这条记录的时候, 外键指向的讲师还没有被添加到Lecture表中, 如果是默认情况下(`NO DEFERABLE`), 那么在执行这条语句之后, 就会立即报错. 但是我们使用的是`DERFRABLE`, 意味着只有当事务结束之后, 才会去检查约束是否满足, 我们可以在同样的事务中把讲师添加到Lecture表中. 也可以在一个事务中设置立即检查`SET CONSTRAINTS UoS_FK IMMEDIATE;`

#### 添加/修改/移除约束

完整性约束可以使用`ALTER TABLE`命令配合一些子命令进行添加, 修改, 移除; 添加, 移除, 重命名, 修改对应的命令是`ADD CONSTRAINT`, `DROP CONSTRAINT`, `RENAME CONSTRAINT`, `ALTER COLUMN`. 

???+ example "例子"

    ```sql
    ALTER TABLE Enrolled ALTER COLUMN grade TYPE VARCHAR(3),
                         ALTER COLUMN mark SET NOT NULL;
    ``` 

如果表中现存的数据不符合新加入的约束的话, 该约束不会被创建.

### 断言 {#assertion}

到目前为止, 我们所定义的约束都是定义在一张表里的. 有一些约束可能无法使用域约束和参与完整性约束描述. 并且有时候需要适用于整个数据库模式的更一般的完整性约束, 这些约束可能会涉及多个表. 

我们可以使用`CREATE ASSERTION`语句来创建断言, 语法为`CREATE ASSERTION <name> CHECK <condition>`. 在创建断言之后, 数据库管理系统会在每次更新数据库的时候检查断言的有效性(即条件必须为真). 这个检查过程可能会显著引入系统开销, 因此需要谨慎使用断言.

???+ example "例子"

    现在, 有一个航海俱乐部, 为了使俱乐部尽可能小, 船只数量和水手数量的和必须小于10, 为此, 有一个同学提出了下列方案:

    ```sql
    CREATE TABLE Sailors (
        sid INTEGER,
        sname CHAR(10),
        rating INTEGER,
        PRIMARY KEY (sid),
        CHECK (rating >=1 AND rating <=10),
        CHECK ((SELECT COUNT(s.sid) FROM Sailors s) + (SELECT COUNT(b.bid) FROM Boats b) < 10)
    )
    ```

    这些代码其实无法实现上述的功能. 问题出在`CHECK`部分. 这里的`CHECK`约束只会在Sailors表插入或者修改数据的时候触发, 但是它不会自动检测Boats表的变化. 这意味着, 比如说, 我向Boats表中增加了很多船只, 只要Sailors表没有变化, 该约束不会被触发, 导致无法有效约束总数小于10. 

    要解决这个问题, 应该使用断言Assertion, 断言的条件可以横跨多张表, 数据库会在每个事务之后检查是否有违反断言的情况.

???+ tip "Tip"

    - SQL不支持"对于所有的X, 条件P(X)成立"的语法, 而且这非常浪费时间. 我们可以对这个式子取反命题, 即"对于所有的X, 条件P(X)成立"等价于"不存在一个X, 使得P(X)不成立", 这个反命题的写法SQL是支持的, 首先, 写一个`SELECT`语句选出所有的违反条件P(X)的元组, 然后使用`NOT EXISTS`语句, 如果返回元组的个数为0, 说明原式成立, 反之, 不成立

        ???+ example "例子"

            假设现在有4个关系: Loan, Borrower, Depositor, 和Account. 定义一个约束使得每一个Loan都有至少一个Borrower的账户中至少有1000刀的现金. 这个式子可以取反命题: "没有一笔Loan是没有任何一个Borrower的账户中至少有1000刀现金的." 对应的断言定义语句为:

            ```sql
            CREATE ASSERTION balance_constraint CHECK (NOT EXISTS
                (
                    SELECT * FROM Loan
                    WHERE NOT EXISTS
                    (
                        SELECT
                            Borrower.loan_number, Borrower.balance FROM Borrower JOIN Depositor ON Borrower.customer_name = Depositor.custom_name JOIN Account ON Depositor.account_number = Account.account_number
                        WHERE
                            Loan.loan_number = Borrower.loan_number
                        AND
                            Account.balance >= 1000
                    )
                )
            )
            ```

            - 如[图](https://img.ricolxwz.io/be08a9f2e269d73038f5e78ec3028264.png), 这个操作是被拒绝的
            - 如[图](https://img.ricolxwz.io/a043d3639a5fd6999bdb4e11235270a3.png), 这个操作是被允许的

    - 虽然断言是一个SQL标准, 但是支持它的DBMs较少, 如Oracle是支持的. 可以用`CHECK`作为替代. PostgreSQL是不支持的

## 动态ICs

### 触发器

动态ICs中, 我们主要来关注触发器. 一个触发器是一段某个条件为真的情况下数据库发生特定的变化时自动执行的代码. 

一个触发器可以分为三个部分:

- 事件: 什么事件激发了触发器
- 条件: 测试条件是否为真, 若为真, 则在事件发生的时候触发行动; 若不为真, 则在事件发生的时候也不触发行动. 需要注意的是不是所有的触发器都有条件, 有的可以没有条件, 只有事件
- 行动: 会发生什么

???+ tip "Tip"

    为什么需要触发器? 断言无法修改数据, 需要一个更加强大的机制来检查条件并且修改数据.

???+ example "例子"

    举一个触发器的例子:

    - 事件: Assessment表发生更新或者插入
    - 条件: Enrolled表中某个学生的mark的总和大于50分
    - 行动: 修改grade的值为'P'

    ```sql
    CREATE TRIGGER gradeEntry
        AFTER INSERT OR UPDATE ON Assessment
        BEGIN
            UPDATE Enrolled E
                SET grade=‘P’
            WHERE ( SELECT SUM(mark)
                FROM Assessment A
                WHERE A.sid=E.sid AND
                    A.uos=E.uosCode ) >= 50;
        END;
    ```

#### 类型

有多种类型的触发器:

- 约束维护: 触发器可以用于维护参与完整性约束和语义完整性约束, 经常和`ON DELETE`和`ON UPDATE`一起使用
- 商业规则: 动态的商业规则可以用触发器描述
- 监控: 对一些感应器的数据做出响应
- 审计
- ...

#### 事件

触发事件可以是`INSERT`, `DELETE`或者`UPDATE`. 其中, 若为`UPDATE`, 还可以限制是哪些属性更新, 如`CREATE TRIGGER overdraft-trigger AFTER UPDATE OF balance ON Account`. 

PostgreSQL在触发`UPDATE`或`DELETE`可以使用`OLD`变量, 代表更新/删除前的行; 在触发`INSERT`或`UPDATE`可以使用`NEW`变量, 这两个变量是自动生成的, 可以直接在触发器内使用.

#### 粒度

触发器的粒度有两种, 一种是行级(row level), 另一种是语句级(statement level). 

- 行级出发器: 这种触发器会对每一行需要更新的数据触发一次, 也就是说, 如果你的SQL语句更新了多行数据, 行级触发器会针对每一行分别执行一次. 例如, 假设你有一条SQL语句更新了10条数据, 那么行级触发器会执行10次, 每次处理一行
- 语句级触发器: 这种触发器在每个触发事件发生时仅仅触发一次, 而不论这次操作影响了多少行数据. 例如, 假设你有一条SQL语句更新了10行数据, 语句级触发器只会在这条SQL语句执行后触发一次

两者之间的详细比较可以见[图](https://img.ricolxwz.io/afff0b0693df1a0fb6ef9a9817294292.png).

##### 行级

行级触发器的语法为: `FOR EACH ROW`.

???+ example "例子"

    ```sql
    CREATE TRIGGER emp_stamp BEFORE INSERT OR UPDATE ON emp
    FOR EACH ROW EXECUTE PROCEDURE emp_stamp();
    ```

如[图](https://img.ricolxwz.io/090a3963ffb6015e442186321013f041.png).

##### 语句级

语句级触发器的语法为: `FOR EACH STATEMENT`.

???+ example "例子"

    ```sql
    CREATE TRIGGER RecordNewAverage AFTER UPDATE OF Salary or INSERT ON Employee
    FOR EACH STATEMENT EXECUTE PROCEDURE Salary_Average();
    ```

如[图](https://img.ricolxwz.io/e54f8653a17c64b34c7828998f459fb5.png).

#### 语法

见[图](https://img.ricolxwz.io/8ea78f6df2632bc7afba00011b8240ba.png).