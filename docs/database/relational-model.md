---
title: 数据库:关系模型
comments: true
---

关系模型(Relational Model)是一种逻辑模型(Logical Model), 逻辑模型是什么详见[这里](/database/conceptual-model/#两类conceptual-model).

## 历史

在1970年之前, 主要使用的逻辑模型是层次模型和网络模型. 层次模型中数据以树状结构组织, 类似于目录结构; 网络模型中数据以图结构组织, 类似于网状结构. 这两种模型都用于早期的数据库系统, 都依赖于底层的计算机硬件结构, 查询和数据操作往往要有深厚的硬件和技术背景, 因此较为复杂, 难以使用.

1970年, IBM的E.F.Codd博士在ACM杂志上发表了论文*A Relation Model for Large Shared Data Banks*, 首次提出了关系模型的概念. 这篇文章触发了数据库管理方面的巨大变革, 他也因此获得了1981年的图灵奖.

## 关系模型

### 关系的概念

关系是一张二维命名的表格. 这个表格由行(又称为元组或记录)和列(又称为属性或字段)组成. 

并非是所有的表格都是关系, 关系需要满足下列条件:

- 关系必须有一个唯一的名字
- 关系中的属性名必须有一个唯一的名字, 列的顺序是不重要的
- 关系中所有的元组必须有相同的结构 
- 所有的属性都是原子类型的, 即每列中的数据是不可再分的基本单位, 如一个人的姓名应该分为"名"和"姓"两个独立的列, 而不是放在一个列中, 这个就是"第一范式"
- 一个关系是元组的集合, 所以每行必须是唯一的, 即不能有两行的所有属性值都相同; 行的顺序是不重要的

???+ tip Tip

    关系型数据库管理系统(RDBMS)在实现关系模型时对数学上的"关系"进行了修改, 具体包括:

    - RDBMS允许重复的行: 在纯粹的数学关系中, 所有的元组(即行)都应该是唯一的, 但在RDBMS中, 允许表格中存在重复的行
    - RDMBS支持对元组和属性进行排序: 数学熵的关系是无序的, 但是在RDBMS中, 元组(行)和属性(列)可以进行排序, 以便更有效地查询和操作数据
    - RDMBS允许用`null`表示缺失/不相关: 数学关系中每个属性应该有一个确切的值, 但是在RDBMS里面, 可以使用`null`值来表示缺失/不相关的信息

        ???+ example "例子"

            - 缺失: 新学生还没有选课
            - 不相关: 兼职教授的年收入是不相关的, 不是正式编制没有年收入
        
        使用`null`的优势是用一个特殊的值表示缺失/不相关可能在某些情景下不好用.

        ???+ example "例子"

            例如, 将工资设置为`-1`表示工资未知. 此时, 计算工资的平均值, 结果就是错误的.

        缺点就是我们必须先忽略所有的`null`, 比较麻烦.

## 使用SQL管理RDBMS

### 创建表

创建表的语法为:

```
CREATE TABLE <table_name> (<column_name> <column_type>, ...)
```

支持的类型有:

| 基本数据类型            | 描述                                                | 示例值                                               |
|-------------------------|-----------------------------------------------------|------------------------------------------------------|
| `SMALLINT` (2 字节)      | 整数值                                              | `1704`, `4070`                                        |
| `INTEGER` (4 字节)       | 整数值                                              | `1704`, `4070`                                        |
| `BIGINT` (8 字节)        | 整数值                                              | `1704`, `4070`                                        |
| `DECIMAL(p,q)`           | 固定精度的数值, 具有 `p` 位精度和 `q` 位小数        | `1003.44`, `160139.9`                                 |
| `NUMERIC(p,q)`           | 固定精度的数值, 具有 `p` 位精度和 `q` 位小数        | `1003.44`, `160139.9`                                 |
| `FLOAT(p)`               | 浮点数, 具有 `p` 位精度                             | `1.5E-4`, `10E20`                                     |
| `REAL`                   | 浮点数                                              | `1.5E-4`, `10E20`                                     |
| `DOUBLE PRECISION`       | 浮点数                                              | `1.5E-4`, `10E20`                                     |
| `CHAR(q)`                | 固定长度为 `q` 的字母数字字符串                     | `'The quick brown fix jumps...'`, `'INFO2120'`        |
| `VARCHAR(q)`             | 可变长度, 长度最多为 `q` 的字母数字字符串           | `'The quick brown fix jumps...'`, `'INFO2120'`        |
| `CLOB(q)`                | 可变长度的字母数字字符串                            | `'The quick brown fix jumps...'`, `'INFO2120'`        |
| `BLOB(r)`                | 大小为 `r` 的二进制字符串                           | `B’01101’`, `X’9E’`                                   |
| `DATE`                   | 日期                                                | `DATE ’1997-06-19’`, `DATE ’2001-08-23’`              |
| `TIME`                   | 时间                                                | `TIME ’20:30:45’`, `TIME ’00:15:30’`                  |
| `TIMESTAMP`              | 时间戳                                              | `TIMESTAMP ’2002-08-23 14:15:00’`                     |
| `INTERVAL`               | 时间间隔                                            | `INTERVAL ’11:15’ HOUR TO MINUTE`                     |

???+ example "例子"

    创建三张表格:

    ```sql
    CREATE TABLE Student (
    sid INTEGER,
    name VARCHAR(20)
    );
    CREATE TABLE Enrolled (
    sid INTEGER, ucode CHAR(8), semester VARCHAR(10)
    );
    CREATE TABLE UnitOfStudy (
    ucode CHAR(8),
    title VARCHAR(30),
    credit_pts INTEGER
    );
    ```

    得到的表格如[图](https://img.ricolxwz.io/e7bd17ea2a47fbe0c29af21a62050751.png).

### 删除表

删除表的语法为:

```
DROP TABLE <table_name>
```

### 修改表

支持对表格做出很多修改, 比如说修改属性名, 增加列, 具体见DBMS提供商的表格. 

修改属性名:

```
ALTER TABLE <table_name> RENAME COLUMN <original_column_name> TO <new_column_name>
```

增加列:

```
ALTER TABLE <table_name> ADD COLUMN <column_name> <column_type>
```

### 插入元组

插入元组的语法为:

```
INSERT INTO <table_name> (<list_of_columns>) VALUES (<list_of_expressions>)
```

???+ example "例子"

    ```sql
    INSERT INTO Student VALUES (12345678, ‘Smith’);
    INSERT INTO Student (name, sid) VALUES (‘Smith’, 12345678);
    ```

### 更新元组

更新元组的语法为:

```
UPDATE <table_name> SET <column_name>=<value>, ... WHERE <column_name>=<value>, ...
```

???+ example "例子"

    ```sql
    UPDATE Student
        SET address = ‘4711 Water Street’
        WHERE sid = 123456789;
    ```

### 删除元组

删除元组的语法为:

```
DELETE FROM <table_name> WHERE <column_name>=<value>, ...
```

???+ example "例子"

    ```sql
    DELETE FROM Student WHERE name="Smith";
    ```

## 键和外键

通常我们说的键, 指的是候选键. 主键是候选键的其中一个.

键应该满足以下条件:

- 唯一性: 在一个关系中, 不能有两个元组的所有键的值都相同
- 最小性: 对于键的子集, 不具有唯一性; 若键的子集具有唯一性, 则它就不是键, 而是超键

在使用SQL语句`CREATE TABLE`的时候, 可以声明键(候选键), 主键, 外键.

- `UNIQUE`语句用于声明候选键
- `PRIMARY KEY`语句用于声明主键
- `FOREIGN KEY`语句用于声明外键

???+ example "例子"

    === "例子1"

        [见图](https://img.ricolxwz.io/97077b1a1099dfb5cf9b58a468008ba6.png)

    === "例子2"

        以`FOREIGN KEY`为例, 默认情况下, 引用的是目标表的主键属性: 

        ```sql
        FOREIGN KEY (sid) REFERENCES Student
        ```

        也可以指定目标表的某一列, 这一列必须是候选键或者主键

        ```sql
        FOREIGN KEY (lecturer) REFERENCES Lecturer(empid)
        ```

## 完整性约束条件 

在[数据模型](/database/conceptual-model/#数据模型的组成要素)中, 我们提到, 数据模型由数据结构, 数据操作和完整性约束三部分组成, 这里关系模型是第二类数据模型, 所以它也有完整性约束.

完整性约束, Integrity Constraints是DBMS中用于确保数据的准确性, 一致性和完整性的一组规则或者条件. 完整性约束的主要目的是防止无效数据进入数据库, 并且确保数据库中的数据始终符合预期的结构和逻辑.

模式(Schema)是数据库的结构或者框架, 完整性约束是在模式定义的时候指定的规则或条件, 当定义一个模式的时候, IC会被明确地声明, 以确保符合预订的结构和规则. 当对数据库中的关系进行修改操作的时候(如插入, 更新, 删除)时, 数据库管理系统会自动检查这些完整性约束, 确保数据的一致性和准确性.

### 重复行IC

在RDBMS中, 是允许插入两条所有属性的值都相同的记录的. 但是这样会比较浪费空间, 而且会造成在更新值的时候, 副本之间的不一致性.

那么如何避免出现重复行呢? 我们可以从键入手:

- 如果表中定义了至少一个键, 那么是否存在两行相同的数据? 答案是不可能的, 因为键的定义要求它的值必须在整个表中唯一. 因此, 如果指定了一个键, 这意味着没有两行数据可以在这个键的所有字段上具有相同的值, 从而避免了重复行的出现
- 如果表中没有指定任何键, 则没有确保行的唯一性, 这就有可能导致表中出现重复的行. 为了解决这个问题, 可以使用`UNIQUE`语句, 将所有的属性作为候选键来确保唯一性. 使用这种方式, 会导致表中的每一行必须在所有的属性的组合上是唯一的, 从而防止了重复行的出现

### 外键IC

对于引用的关系中每个外键值为$\alpha$的元组, 一定要在被引用的关系中存在一个候选键也为$\alpha$的元组, 如[图](https://img.ricolxwz.io/3578df3777540c7e36266edb3b958db2.png).

### 非空IC

RDBMS在默认情况下允许用`null`表示缺失/不相关. 对于某一些应用, 声明某些属性的值不能为`null`是至关重要的. 在SQL中, 可以用`NOT NULL`表示这个属性不能取`null`.

???+ example "例子"

    ```sql
    CREATE TABLE Student (
        sid
        INTEGER NOT NULL,
        name
        VARCHAR(20) NOT NULL,
        login
        VARCHAR(20) NOT NULL,
        gender CHAR,
        birthdate DATE
    );
    ```

#### 键和非空IC

- 主键
    - 一张表最多有一个, 它的值必须是唯一的
    - 自动声明为`NOT NULL`
- 键(候选键)
    - 一张表可能有多个, 若声明要使用`UNIQUE`
    - 可能有`NULL`的值
- 外键
    - 默认允许`NULL`
    - 在某些场景下, 某些记录可能没有关联的父记录. 这种情况下, 外键字段可以设置为允许`NULL`. 如一个员工表可能有一个外键字段指向经理的ID, 但不是每个员工都有经理, 如CEO没有经理, 因此外键字段可以设置为`NULL`

## 将ERD映射到关系模型

在上节我们讲到, ERD表示的是概念模型, 是第一类模型; 而关系模型是第二类模型. 我们在定义完成第一类模型之后, 需要将其转化到逻辑模型, 在这里即关系模型, 幸好, 有这么一种映射机制可以将ERD映射到关系模型.

### 映射强实体型

什么是强实体型, 见[这里](/database/conceptual-model/#强弱实体型).

在ERD中, 所有的强实体型都会变成一个关系. 列对应属性, 行对应实体. 

对于属性来说, 映射需要看情况:

- 简单属性: 直接将ER的属性映射到关系中
- 复合属性: 将ER的复合属性分解后各个属性以简单属性的方式映射到关系中
- 多值属性: 需要一个独立的关系来表示这些多值属性, 通过外键和含有实体的关系连接

???+ tip "Tip"

    复合属性和多值属性的本质区别就是复合属性中有多少个小属性是固定的, 但是多值属性中有多少个小属性是不固定的. 如地址是一个复合属性, 它由街道, 城市, 邮政编码组成; 如学生的所选是一个多值属性, 因为可以选不定数量的课程.

### 映射没有约束的关系

没有约束的关系即对于实体集和某一个关系来说, 实体集没有键约束, 参与约束, 基数约束. 想要映射这种关系特别简单, 只要将实体集的主键的组合作为新的关系的主键就行了. 如[图](https://img.ricolxwz.io/f7a07b8706af6f4dab96d5a946ee93a2.png).

### 映射有约束的关系 {#map-constraints}

#### 映射有键约束的关系 

什么是键约束, 见[这里](/database/conceptual-model/#键约束).

可以将参与关系的实体集的关系和关系集的关系组合变成一个新的关系. 太复杂了....直接看[图](https://img.ricolxwz.io/c8203c4430ba88d59b0ccb708c07a162.png).

若要表示两侧都有键约束, 可以在外键上施加一个唯一性限制. 直接看[图](https://img.ricolxwz.io/d528c111b390896090bb774e9fd92fab.png).

我们要在`Employee`关系的`did`字段上施加一个唯一性限制, 表示每一个元组的`did`字段的值都不一样, 这就导致每一个部门只能有一个员工, 每一个员工只能属于一个部门.

#### 映射有键约束和参与约束的关系

什么是键约束, 见[这里](/database/conceptual-model/#键约束). 什么是参与约束, 见[这里](/database/conceptual-model/#participation-constraints).

我们以两侧都有键约束为例, 现在在一侧加入一个参与约束, 要实现将这个参与约束映射到关系中, 就要使得这个外键不为空, 即为`NOT NULL`. 根据上面讲到的, 要实现两侧的键约束, 外键还需要是唯一的, 所以外键: 1. 既是唯一的; 2. 又是非空的. 见[图](https://img.ricolxwz.io/fca7486e063b1bc75f1ef25d31873e46.png).

### 映射弱实体型 {#map-weakstrongentity}

什么是弱实体型, 见[这里](/database/conceptual-model/#强弱实体型).

弱实体型映射到一个主键是区分符和强实体型的主键的组合的关系中. 如[图](https://img.ricolxwz.io/ec2b4323b6856140eea624640c405c24.png).

其中, 弱实体型映射的关系的主键是一个复合主键, 包含强实体型关系的主键`empID`和区分符`given`和`family`.

### 映射泛化结构 {#map-isa}

什么是isA结构(泛化/反泛化), 见[这里](/database/conceptual-model/#泛化反泛化).

映射isA结构的时候, 子类的外键是超类(高层次的, 抽象的类)的主键. 如[图](https://img.ricolxwz.io/e24aee851049a321ea87670a3368daf6.png)

### 映射聚合

聚合之后的新的实体型的键和另一个参与聚合关系的实体的键构成了聚合关系的键和外键. 如[图](https://img.ricolxwz.io/e5f435a531088490c3c6c0eb1ce55426.png).