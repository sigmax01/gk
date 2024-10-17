---
title: 数据库:应用开发
comments: true
---

## 交互式和非交互式SQL

交互式SQL, 用户通过命令行或者图形几面的SQL客户端与数据库进行交互, 实时输入SQL语句并获取结果. 用户可以逐条执行SQL命令, 比立即看到执行结果, 交互式SQL主要用于用于数据库的管理, 调试, 数据查询或者临时操作.

非交互式SQL, SQL语句以脚本或者嵌入的方式提交给数据库执行, 通常不需要用户的实时参与. 非交互式SQL可以通过编程语言的数据库库调用, 如Python的pymysql, Java的JDBC等, 或者通过预先写好的SQL脚本. SQL命令被预先定义好并批量执行.

## 架构

### 单层架构

单层架构, 或称集中式系统, Centralized System, 通常指的是客户端, 应用程序逻辑和数据库管理系统全都集成在一个应用程序中. 这种架构通常适用于有一个集成数据库的应用, 如MS Access或者SQLite, 特别是在智能手机应用中. 

在这种架构中, 客户端同时负责以下的所有服务:

- Presentation服务: 负责展示表单和数据输入输出的用户界面
- Application服务: 实现用户请求并与DBMS进行交互
- DBMS: 处理数据库操作请求, 如查询, 插入, 更新和删除

### 双层架构

双层架构, 或称客户端-服务端模型. 在这种架构中, 客户端负责Presentation服务和Application服务, 而服务端负责处理来自客户端的请求, 即有一个DBMS服务. 客户端通过网络向数据库服务器发送查询或者更新请求, 数据库服务器处理请求后返回结果. 通常用于小型或者中等规模的应用程序, 尤其是数据库直接访问的场景. 

### 三层架构

三层架构加了一层中间层, 将应用逻辑即Application服务与用户界面即Presentation服务和数据库管理即DBMS分离. 客户端专注于用户界面和数据展示, 减少客户端的业务逻辑处理量. 中间层负责业务逻辑和处理复杂的应用操作, 它接受来自客户端的请求, 经过逻辑处理, 与数据库管理层通信, 返回结果. 数据库管理层, 即数据库服务器, 负责数据的存储和查询的执行. 这种架构适合大型应用和分布式系统, 层和层之间的通信都是通过网络进行的. 

## 应用开发

### 宿主语言调用SQL

编程语言如C++, Java, PHP, Python都可以在编程语言中调用SQL命令, 并且可以直接引用宿主语言中的变量. 但是在调用之前, 必须确保数据库的连接. 

在宿主语言中调用SQL主要有两种方法: 

- Statement-level Interface (SLI): SQL语句被嵌入到宿主语言中
- Call-level Interface (CLI): 通过调用库的API来间接调用SQL, 典型的例子有JDBC, SQL语句作为字符串传递给JDBC的API函数, 然后JDBC帮你调用. 这种方法的好处是提供了一层抽象的接口, 我们不需要关系底层的数据库是什么类型, 无论是PostgreSQL, 还是MySQL, 只要用一个JDBC的API函数去调用, 效果都是一样的

### JDBC

JDBC是一个Java的API, 用于与支持SQL的数据库系统进行通信, 它支持多种用于查询和更新数据以及检索查询结果的功能. 通过JDBC和数据库交互的过程可以总结为:

1. 获取连接: 首先, 需要连接到数据库. 这通常涉及创建数据库连接对象, 通过提供数据库的URL, 用户名和密码, 连接到数据库服务器
2. 创建`Statement`对象: 一旦连接成功, 需要创建一个`Statement`对象, 这是发送SQL查询到数据库的对象
3. 使用`Statement`对象发送SQL查询并从数据库获取查询结果
4. 使用异常机制处理错误

#### 架构

JDBC是与数据库管理系统无关的, JDBC是编程语言与DBMS之间的一个抽象层. 这意味着无论你使用哪种数据库, 都已通过相同的API来进行操作. 以下是一个SQL请求通过JDBC的执行过程.

1. 应用程序通过JDBC的API发送请求, SQL语句会作为一个参数传递给JDBC的接口
2. 驱动管理器会根据连接中数据库的类型, 选择正确的驱动
3. 驱动将通用的API调用转换为具体的数据库操作, 每种数据库都有自己的驱动程序
4. 数据库操作被发送到相应的数据库, 执行并返回结果

#### 连接到数据库

可以使用`DriverManager`的`getConnection`方法, 传递数据库的URL, 用户名和密码来获取数据库连接对象`Connection`, 不同的数据库有不同的URL格式.

???+ example "例子"

    以PostgreSQL为例, 可以写为.

    ```java
    String url = "jdbc:postgresql://localhost:5432/mydatabase";
    String user = "postgres";
    String password = "password";
    Connection conn = DriverManager.getConnection(url, user, password);
    ```

???+ warning "注意"

    最后, 要始终使用`conn.close()`释放资源.

#### 执行查询

在执行SQL查询之前, 需要通过先前已有的数据库连接对象创建`Statement`对象, 这个对象是用来执行SQL语句的接口.

???+ example "例子"

    从`Connection`对象创建`Statement`对象.

    ```java
    Statement stmt = conn.createStatement();
    ```

    使用`executeQuery`方法来执行SQL查询, 并返回一个`Resultset`对象.

    ```java
    ResultSet rs = stmt.executeQuery("SELECT * FROM students");
    ```

    或者可以用`executeUpdate()`执行DML操作(`INSERT`, `UPDATE`, `DELETE`), 返回收到影响的行数.

    ```java
    int rowsAffected = stmt.executeUpdate("INSERT INTO students (name, age) VALUES ('John', 20)");
    ```

???+ warning "注意"

    在执行完SQL操作后, 应该关闭`Statement`对象释放资源, `stmt.close()`.

#### 检索结果

`stmt.executeQuery`返回的结果会封装在`ResultSet`对象中, 它其实是一个强大的"游标", 可以实现的功能有:

- `previous()`: 将游标移动到上一行
- `absolute(<num>)`: 将游标移动到指定行号的那一行
- `relative(<num>)`: 相对于当前位置, 向前或者向后移动指定的行数
- `first()`/`last()`: 直接跳转到结果的第一行或者最后一行
- `wasNull()`: 处理空值

##### 流式处理

注意, 结果集`ResultSet`不会一次性fetch所有的数据, 关于什么是fetch, 在[DB-API的流式处理](#流式处理)有非常详细的解释. 结果是随着你调用`next()`, `previous()`等方法的时候, 逐行从数据库服务器获取的.

#### 处理错误

许多SQL操作在发生错误的时候会抛出一个`SQLException`, 通过`catch(SQLException e){...}`抓取错误, 然后通过`e.getMessage()`, `e.getSQLState()`, `e.getErrorCode()`查看问题所在. 除了这个错误之外, 还可以抓取的子错误类型有`SQLTimeoutExceptino`, `SQLIntegrityConstraintViolationException`.

`SQLWaning`是`SQLException`的一个子类, 它不如`SQLException`那么严重. 

???+ example "例子"

    ```java
    void exampleEnrolment() {
        Connection conn = null;
        try {
        conn = openConnection();
        Statement stmt = conn.createStatement();
        stmt.executeUpdate("INSERT INTO Transcript VALUES (123,’COMP9120', ‘S1', 2024,'HD')");
    }
    catch (SQLIntegrityConstraintViolationException e) {
        System.err.println("Violated a constraint!”);
    }
    catch (SQLTimeoutException e) {
        System.err.println("Operation timed out");
    }
    catch (SQLException e) {
        System.err.println("Other problem");
    }
    finally {
        if (conn != null)
            try{conn.close();} catch(SQLException e) {//handle exception}
        }
    }
    ```

#### Java和SQL类型匹配

| SQL Type   | Java class           | ResultSet get method |
|------------|----------------------|----------------------|
| BIT        | Boolean              | getBoolean()         |
| CHAR       | String               | getString()          |
| VARCHAR    | String               | getString()          |
| DOUBLE     | Double               | getDouble()          |
| FLOAT      | Double               | getDouble()          |
| INTEGER    | Integer              | getInt()             |
| REAL       | Double               | getFloat()           |
| DATE       | java.sql.Date        | getDate()            |
| TIME       | java.sql.Time        | getTime()            |
| TIMESTAMP  | java.sql.Timestamp   | getTimestamp()       |

### DB-API {#DB-API}

DB-API是Python用于和支持SQL的数据库通信的API, 每个数据库引擎如Oracle, PostgreSQL, IBM DB2会有特定模块提供DB-API功能的实现. 即DB-API是Interface, 数据库引擎的相关模块是Implementation. 以下是一个SQL请求通过DB-API的执行过程.

1. 获取连接
2. 创建一个游标对象
3. 使用游标对象发送查询并获取结果
4. 处理异常

???+ example "例子"

    ```py
    import psycopg2
    try:
        # 获取连接对象以连接数据库
        conn = psycopg2.connect(database="postgres", user="test", password="secret", host="host")
        # 获取游标以准备查询数据库
        curs = conn.cursor()
        # 执行SQL查询
        curs.execute("SELECT name
                    FROM Student NATURAL JOIN Enrolled
                    WHERE uos_code = "COMP9120")
        # 循环遍历结果, 每一行是一个元组
        for result in curs:
            print("student: " + result[0])
        # 释放游标和连接
        curs.close()
        conn.close()
    except Exception as e:
        print("SQL error: unable to connect to database or execute query")
        print(e)
    ```

#### 常用游标方法

- `execute(<operation>, <param1, param2, ...>)`: 执行一个SQL查询或其他命令, `<operation>`是包含SQL语句的字符串, `<pram1, param2, ...>`是可选的参数, 用于在查询中替换占位符(参数化查询), 如`curs.execute("SELECT * FROM students WHERE id = %s", (123,))`
- `executemany`: 可以执行相同的查询或其他命令多次, 每次使用不同的参数, 适合批量插入或者更新数据. 如`curs.executemany("INSERT INTO students (name, age) VALUES (%s, %s), [('john', 20), ('Doe', 22)])`
- `fetchone()`: 从查询结果中获取下一行, 如果没有更多的数据的话返回`None`, 适合只获取单条结果的场景
- `fetchmany(<size=cursor.arraysize>)`: 从查询结果中获取多行, `<size>`指定返回的行数, 如果不指定, 默认返回`cursor.arraysize`行, 适合需要一次性获取多行数据的场景
- `fetchall()`: 获取查询结果中所有的剩余行
- `close()`: 释放游标资源

##### 流式处理 {#流式处理}

细心的同学可能会问: `curs`不是已经拿到结果了吗, 为什么还要fetch? 这是因为游标只是一个查询工具, 把命令发给数据库服务器. 结果其实是在数据库服务器生成的, 而不是在应用服务器生成的, 这个fetch相当于发出了一个请求, 请求数据库服务器把对应行的数据发过来, 而且如果数据库返回的结果非常大, 比如上百万行数据, 如果直接读取到应用服务器, 会占用大量的带宽, 而且会占用大量内存, 导致性能下降.

#### 处理错误

可以通过Python的异常处理机制处理错误. 用到的是`psycopg2.Warning`和`psycopg2.Error`两类. 可以进一步通过`e.pgerror`和`e.pgcode`分别查看数据库返回的错误消息和SQL状态代码.

## 安全

### SQL注入

SQL注入, SQL Injection是一种常见的网路攻击技术, 攻击者通过将恶意的SQL代码插入到应用程序的输入中, 从而改变原本预期的SQL查询执行行文, 这通常发生在未对用户输入进行充分验证和过滤的情况下, 导致攻击者能够执行任意的SQL命令, 如读取, 修改, 删除数据库中的数据, 甚至控制数据库服务器.

SQL注入攻击的基本原理是利用应用程序将用户输入直接插入到SQL查询中的漏洞. 攻击者通过在输入中插入特定的SQL语句, 试图操纵SQL查询结构, 使其执行意图之外的操作.

???+ example "例子"

    === "Java"

        假设有一个简单的登录系统, 使用用户提供的用户名和密码来查询数据库中的数据验证登录.

        ```java
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(
            "SELECT * FROM Student WHERE name = '" + uName + "' AND Pass ='" + uPass + "'")
        ```

        攻击者可以在输入框中输入以下内容来进行SQL注入:

        - 用户名: `' OR '1'='1`
        - 密码: `' OR '1'='1`

        生成的查询语句变为:

        ```sql
        SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '' OR '1'='1';
        ```

        在这种情况下, `'1'='1'`总是为真, SQL查询会返回数据库中的所有用户信息, 允许攻击者绕过身份验证.

    === "Python"

        ```python
        query = """SELECT E.studId FROM Enrolled E
            WHERE E.uosCode = """ + uosCode + 
            " AND E.semester = " + semester
        cursor.execute(query)
        ```

        攻击者输入:

        - `uosCode`: `123 OR '1'='1`
        - `semester`: `' OR '1'='1`

        生成的查询语句变为:

        ```sql
        SELECT E.studId FROM Enrolled E WHERE E.uosCode = 123 OR '1'='1' AND E.semester = '' OR '1'='1';
        ```

常见的解决方法有:

- 隐藏错误信息: 错误信息能够意外暴露底层数据库的一些敏感信息, 如数据库的结构, 代码
- 存储加盐哈希后的密码: 详情见[这里](https://py.ricolxwz.de/%E5%B8%B8%E7%94%A8/hmac/), 使用常见的哈希算法, 如bcrypt, argon2, pbkdf2, 然后随机加入一个值(盐), 这会保护数据库免收彩虹表攻击, 确保密码一样的情况下, 存储在数据库的值都不同
- 在Java中使用预处理语句
- 在Python中使用匿名或者命名参数

#### 预处理语句

在Java中, 使用`PreparedStatement`即预处理语句可以防止SQL注入. 即使用户输入了类似`' OR '1'='1`的内容, 它也只会被视作一个字符串, 不会影响SQL查询的逻辑. 

???+ example "例子"

    ```java
    stmt.conn.prepareStatement("UPDATE account
                                SET balance = balance + ?
                                WHERE account_number = ?");
    stmt.setFloat(1, amount);
    stmt.setInt(2, accountno);
    result = stmt.executeQuery();
    ```

#### 匿名或者命名参数

`execute()`会自动对参数进行必要的转义和类型转换, 而不会直接影响查询的逻辑结构.

???+ example "例子"

    === "匿名参数"

        ```py
        studid = 12345
        cursor.execute(
            "SELECT name FROM Student WHERE sid=%s",
            (studid,)
        )
        ```

    === "命名参数"

        ```py
        studid = 12345
        cursor.execute(
            "SELECT name FROM Student WHERE sid=%(sid)s",
            {'sid': studid}
        )
        ```

## 存储过程

存储过程, stored procedure, 是在大型数据库系统中, 一组为了完成特定功能的SQL语句集. 经过编译创建并保留在数据库中, 用户可以通过存储过程的名字并给定参数来调用执行. 如[图](https://img.ricolxwz.io/046d2f1f099f461536ae9ecd2529d8e5.png)所示, 下面的部分就是存储过程的架构示意图.

优点: 

- 额外的抽象层: 程序员不需要知道数据库的详细结构, 只需要调用存储过程
- 减少数据传输: 存储过程可以在数据库服务器上处理复杂逻辑, 而不是在应用服务器, 减少了应用程序和数据库之间的数据传输量, 有助于提高性能, 特别是在网络带宽受限的情况下

缺点:

- 迁移问题: 如果需要更换DBMS, 存储过程可能需要重写, 不同的DBMS有不同的存储过程和执行方式, 因此迁移数据库会带来较大的工作量

### SQL/PSM标准

SQL/PSM是一种扩展SQL标准的语言, 用于编写存储过程和函数, 它为SQL提供了类似于编程语言的功能, 允许用户在数据库中编写逻辑控制, 声明变量, 循环和条件语句等, 它的主要目标是将逻辑处理移到数据库中, 而不是在应用程序代码中执行, 进而减少通信开销. 不同的DBMS对于SQL/PSM的支持程度不同, 例如PostgreSQL的PL/pgSQL, 它基于SQL/PSM但是加入了一些PostgreSQL的特性; Oracle的PL/SQL, 基于SQL/PSM加入了一些Oracle的特性, 所有各个数据库厂商对与SQL/PSM的实现会有不同.

存储过程可以接受合法的SQL类型参数, 主要有三种参数模式:

- `IN`: 用于传递给存储过程的参数
- `OUT`: 用于接受存储过程返回值的参数
- `INOUT`: 同时用于传递给存储过程和接受存储过程返回值的参数

#### PL/pgSQL

???+ example "例子"

    ```sql
    CREATE FUNCTION RateStudent(studId INTEGER, uos VARCHAR) RETURNS CHAR AS $$
    DECLARE
        grade CHAR;
        marks INTEGER;
    BEGIN
        SELECT SUM(mark) INTO marks
        FROM Assessment
        WHERE sid=studId AND uosCode=uos;
        IF marks>=85 THEN grade := ‘H’;
        ELSIF marks>=75 THEN grade := ‘D’;
        ELSIF marks>=65 THEN grade := ‘C’;
        ELSIF marks>=50 THEN grade := ‘P’;
        ELSE grade := ‘F’;
        END IF;
        RETURN grade;
    END; $$ LANGUAGE plpgsql;
    ```

### 调用

#### 使用JDBC

可以用`Statement`类的子类`CallableStatement`.

???+ example "例子"

    === "调用有返回值的存储过程"

        ```sql
        CallableStatement call = conn.prepareCall(”{? = call RateStudent(?, ?)}");
        call.registerOutParameter(1, Types.CHAR);
        call.setInt(2, 101);
        call.setString(3, "COMP9120");
        call.execute();
        String result = call.getString(1)
        ```

    === "调用有IN/OUT参数的存储过程"

        ```sql
        CallableStatement call = conn.prepareCall(”{call RateStudent_INOUT(?, ?, ?)}");
        call.setInt(1, 101);
        call.setString(2, "COMP9120");
        call.registerOutParameter(3, Types.CHAR);
        call.execute();
        String result = call.getString(3)
        ```

#### 使用DB-API

游标对象有一个特别的`callproc()`方法

???+ example "例子"

    === "调用有返回值的存储过程"

        ```sql
        curs.callproc(“RateStudent”, [101, "comp9120"])
        output = curs.fetchone()
        result = output[0]
        ```

    === "调用有IN/OUT参数的存储过程"

        ```sql
        curs.callproc(“RateStudent_INOUT”, [101, "comp9120"])
        output = curs.fetchone()
        result = output[0]
        ```
