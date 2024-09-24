---
title: 信息论:关系代数
comments: true
---

关系代数(Relational Algebra)是一种基于集合论的数学理论, 用于对关系数据库中的数据进行建模和查询. 它由埃德加·F·科德(Edgar F. Codd)提出, 提供了一套运算符, 这些运算符可以对一个或者多个关系进行操作, 生成新的关系作为结果. 

## 运算符

关系代数的运算符包括:

- 一元运算符, Unary Operator
    - 选择(σ): 从关系中选择符合条件的元组
    - 投影(π): 从关系中选择某些列
    - 重命名(ρ): 重命名属性或者关系
- 二元运算符, Binary Operator
    - 连接操作符 
        - 笛卡尔积(×): 将两个关系中所有元组组合起来, 形成一个新的关系
        - 连接(⋈): 将两个关系中匹配的元组组合起来, 通常会基于共同的属性进行匹配
    - 集合操作符
        - 并(∪): 返回关系A和B中所有元素的并集, 包含A和B中所有的元素, 不重复
        - 交(∩): 返回关系A和B中同时存在的元组
        - 差(-): 返回只在关系A中存在而不在关系B中存在的元组

这些运算符可以组合使用, 以表达更加复杂的查询. 关系代数描述了得到答案的详细步骤, 因此它是一种过程式语言. 元组演算相比之下是一种声明式语言, 描述的是最终状态的结果. SQL是声明式的. 

其实, 只有6种基本运算符, 分别是σ, π, ×, ∪, -, ρ. 其他的都是衍生的运算符, 如⋈Θ, 其实可以表示为R ⋈Θ S = σΘ(R×S)...

### 选择条件

在数据查询和筛选中, 选择条件通常是由许多个条件组合而成的布尔表达式. 这些条件用于过滤数据集, 以便根据特定的标准选择数据. 每个术语可以是以下两种形式之一: 

- 属性和常量之间的比较: `attribute op constant`
- 属性之间的比较: `attribute1 op attribute2`

可用的运算符包括:

- `<`: 小于
- `>`: 大于
- `<=`: 小于或等于 
- `>=`: 大于或等于 
- `≠`: 不等于
- `=`: 等于

选择条件可以通过布尔运算符进行组合, 以便形成更加复杂的查询条件:

- `^`: AND
- `∨`: OR

### 笛卡尔积

笛卡尔积, 又可以叫作Cartesian Product. 可以被表示为RxS = {ts|t∈R∧s∈S}. 也就是说, R中的每一个元组都会和S中的每一个元组配对. 如[图](https://img.ricolxwz.io/41fb587e0c524889d69f3d1782c3f266.png).

???+ example "例子"

    现在, 有两张表:

    | EmpID | EmpName | DeptID |
    |-------|---------|--------|
    | 1     | Alice   | 10     |
    | 2     | Bob     | 20     |
    | 3     | Charlie | 10     |

    | DeptID | DeptName    |
    |--------|-------------|
    | 10     | HR          |
    | 20     | Engineering |

    对这两张表进行笛卡尔积操作Employees×Departments, 得到的表为:

    | EmpID | EmpName | DeptID | DeptID | DeptName    |
    |-------|---------|------------------|--------------------|-------------|
    | 1     | Alice   | 10               | 10                 | HR          |
    | 1     | Alice   | 10               | 20                 | Engineering |
    | 2     | Bob     | 20               | 10                 | HR          |
    | 2     | Bob     | 20               | 20                 | Engineering |
    | 3     | Charlie | 10               | 10                 | HR          |
    | 3     | Charlie | 10               | 20                 | Engineering |

#### 条件连接 {#条件连接}

条件连接, 又叫作Θ连接. 是在笛卡尔积的基础上再加上一个选择运算符. R ⋈Θ S = σΘ (R×S). 如[图](https://img.ricolxwz.io/bd426ebd66d36ac36fefbdf04429db34.png).

???+ tip "Tip"

    条件连接有四种类型: 

    - 内连接
    - 左外连接
    - 右外连接
    - 全外连接

    如[图](https://img.ricolxwz.io/544a3baef5ea8d499660dacdd610aa38.png).

    默认的条件连接为内连接.

    ???+ example "例子"

        === "内连接"

            现在有两张表A和B.

            | CustomerID | CustomerName |
            |------------|--------------|
            | 1          | Alice        |
            | 2          | Bob          |
            | 3          | Charlie      |

            | OrderID | CustomerID | Product    |
            |---------|------------|------------|
            | 101     | 1          | Laptop     |
            | 102     | 2          | Smartphone |
            | 103     | 4          | Tablet     |

            他们的内连接`INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID`是:

            | CustomerID | CustomerName | CustomerID | OrderID | Product    |
            |----------------------|--------------|-------------------|---------|------------|
            | 1                    | Alice        | 1                 | 101     | Laptop     |
            | 2                    | Bob          | 2                 | 102     | Smartphone |

            可以看到, 结果表中的元组必须严格符合内连接的定义.

        === "左外连接"

            现在有两张表A和B.

            | CustomerID | CustomerName |
            |------------|--------------|
            | 1          | Alice        |
            | 2          | Bob          |
            | 3          | Charlie      |

            | OrderID | CustomerID | Product    |
            |---------|------------|------------|
            | 101     | 1          | Laptop     |
            | 102     | 2          | Smartphone |
            | 103     | 4          | Tablet     |

            他们的左外连接`LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID`是:

            | CustomerID | CustomerName | CustomerID | OrderID | Product    |
            |----------------------|--------------|-------------------|---------|------------|
            | 1                    | Alice        | 1                 | 101     | Laptop     |
            | 2                    | Bob          | 2                 | 102     | Smartphone |
            | 3                    | Charlie      | NULL              | NULL    | NULL       |

            可以看到, 在包含内连接那些元组的基础上, 还包含来自A中`CustomerID`在B中`CustomerID`找不到的元组, 找不到所有的属性填充为`NULL`.

        === "右外连接"
        
            现在有两张表A和B.

            | CustomerID | CustomerName |
            |------------|--------------|
            | 1          | Alice        |
            | 2          | Bob          |
            | 3          | Charlie      |

            | OrderID | CustomerID | Product    |
            |---------|------------|------------|
            | 101     | 1          | Laptop     |
            | 102     | 2          | Smartphone |
            | 103     | 4          | Tablet     |

            他们的右外连接是:

            | CustomerID | CustomerName | CustomerID | OrderID | Product    |
            |----------------------|--------------|-------------------|---------|------------|
            | 1                    | Alice        | 1                 | 101     | Laptop     |
            | 2                    | Bob          | 2                 | 102     | Smartphone |
            | NULL                 | NULL         | 4                 | 103     | Tablet     |

            可以看到, 在包含内连接那些元组的基础上, 还包含来自B中`CustomerID`在A中`CustomerID`找不到的元组, 找不到所有的属性填充为`NULL`.

        === "全外连接"

            现在有两张表A和B.

            | CustomerID | CustomerName |
            |------------|--------------|
            | 1          | Alice        |
            | 2          | Bob          |
            | 3          | Charlie      |

            | OrderID | CustomerID | Product    |
            |---------|------------|------------|
            | 101     | 1          | Laptop     |
            | 102     | 2          | Smartphone |
            | 103     | 4          | Tablet     |

            他们的全外连接是:

            | CustomerID | CustomerName | CustomerID | OrderID | Product    |
            |----------------------|--------------|-------------------|---------|------------|
            | 1                    | Alice        | 1                 | 101     | Laptop     |
            | 2                    | Bob          | 2                 | 102     | Smartphone |
            | 3                    | Charlie      | NULL              | NULL    | NULL       |
            | NULL                 | NULL         | 4                 | 103     | Tablet     |

            可以看到, 在包含内连接那些元组的基础上, 还包含来自A中`CustomerID`在B中`CustomerID`找不到的元组, 找不到所有的属性填充为`NULL`. 还包含来自B中`CustomerID`在A中`CustomerID`找不到的元组, 找不到所有的属性填充为`NULL`.

##### 等值连接

等值连接, Equi-Join是一种条件连接的特殊情况, 它在条件连接的基础之上, 又明确了条件中必须只含有等于号.

???+ example "例子"

    现在, 有两张表:

    | EmpID | EmpName | DeptID |
    |-------|---------|--------|
    | 1     | Alice   | 10     |
    | 2     | Bob     | 20     |
    | 3     | Charlie | 10     |

    | DeptID | DeptName    |
    |--------|-------------|
    | 10     | HR          |
    | 20     | Engineering |

    对两张表进行等值连接: Employees⋈(Employees.DeptID=Departments.DeptID)​Departments, 得到的表为:

    | EmpID | EmpName | DeptID | DeptID | DeptName    |
    |-------|---------|--------------------|----------------------|-------------|
    | 1     | Alice   | 10                 | 10                   | HR          |
    | 3     | Charlie | 10                 | 10                   | HR          |
    | 2     | Bob     | 20                 | 20                   | Engineering |

###### 自然连接

自然连接, Natural Join是一种等值连接的特殊情况, 它在等值连接的基础之上, 又明确了对于所有的名字相同的属性都进行等值连接, 并且只保留其中的一列. 

???+ example "例子"

    现在, 有两张表:

    | EmpID | EmpName | DeptID |
    |-------|---------|--------|
    | 1     | Alice   | 10     |
    | 2     | Bob     | 20     |
    | 3     | Charlie | 10     |

    | DeptID | DeptName    |
    |--------|-------------|
    | 10     | HR          |
    | 20     | Engineering |

    对两张表进行自然连接: Employees⋈​Departments, 得到的表为:

    | EmpID | EmpName | DeptID | DeptName    |
    |-------|---------|--------|-------------|
    | 1     | Alice   | 10     | HR          |
    | 3     | Charlie | 10     | HR          |
    | 2     | Bob     | 20     | Engineering |

    另外还有例子, 如[图](https://img.ricolxwz.io/5f27225a266af62d76910969c2f42ce4.png).

### 集合

集合操作和笛卡尔积等连接操作有很大区别. 集合操作要求两个参与的关系必须有相同的结构, 即类的数量和类型必须相同. 以Union集合操作为例, 结果表的结构和原始表的结构相同, 列的数量和类型都保持一致, 结果集合的行数是两个集合中所有行的综合(去除重复行后); 笛卡尔积的结果表的结构是两个原始表的结构的组合, 列的数量是两个原始表的列数的综合(不考虑自然连接), 结果表的行数是两个原始表的行数的乘积.

举一个例子, 如[图](https://img.ricolxwz.io/56e947249dad059e89bf9fca117c7c88.png).

### 重命名

重命名操作不会修改原始表, 而是产生一个新的表或者关系的"副本", 该副本具有新的名称/或属性名, 原始表的名称和属性名不会因为重命名操作而发生改变.

???+ example "例子"

    假设我们有一个关系 employee, 它的属性有 empid, name, age, department. 如果我们使用重命名操作ρemp_info​(employee), 那么这个操作的结果是将 employee 这个关系命名为 emp_info, 但它的属性名保持不变. 结果可以表示为emp_info(empid, name, age, department). 
    
    再举一个例子, 如果我们使用带有属性名和表名的重名名操作ρemp_info​(eid,ename,eage,dept)(employee), 么这个操作不仅将 employee 这个关系命名为 emp_info, 而且还将它的属性名称分别重命名为 eid, ename, eage, 和 dept. 结果可以表示为: emp_info(eid, ename, eage, dept)

## RA在RDBMS中的角色 {#RA在RDBMS中的角色}

1. 用户发出一个声明式的查询, 也就是我们常写的SQL语句
2. SQL查询被解析器解析, 转为关系代数表达式
3. 查询优化器对关系代数表达器进行优化, 寻找逻辑上等价但是更有效率的表达方式
4. 优化后的关系代数表达式被转换为查询执行计划, 这是一种低层次的描述, 说明如何具体执行查询
5. 查询执行计划被转换为可执行代码
6. 最后生成的代码在数据库引擎中执行, 以实际获取查询结果

如[图](https://img.ricolxwz.io/79349016c11055718d8ce3bc39138192.png).