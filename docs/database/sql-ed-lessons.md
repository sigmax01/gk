---
title: 数据库:SQL课程
comments: true
---

- 不要用`"`, 双引号在SQL中有不同的含义
- 在单引号里面是大小写敏感的, 但是SQL的关键字本身是不敏感的
- 对于`count`函数, 如果传入的参数是`*`, 则统计该表的总行数(不管有没有缺失值), 如果传入的参数是某一个属性名, 则统计的是该属性中除去缺失值之外的个数, `MAX`, `AVG`等会自动忽略缺失值
- `INSERT INTO <table> VALUES <values>`, `UPDATE <table> SET <values> WHERE <conditions>`, `DELETE FROM <table> WHERE <conditions>`
- `CREATE TABLE <table> (<attr1>, <type1>, ...)`, 注意`PRIMARY KEY`, `NOT NULL`, `DEFAULT <default_value>`, `references <table>(<attr>)`的使用, 以及`DROP TABLE`

    ???+ example "例子"

        === "案例1"

            ```sql
            create table Person (
                license integer primary key, -- 不要漏逗号
                name varchar(50) not null
            ); -- 不要漏分号

            create table Car (
                regno char(6) primary key,
                model varchar(30),
                driver integer references person(license)
            );
            ```

        === "案例2"

            ```sql
            create table Studio (
                studio_id integer primary key,
                name varchar(50) not null,
                address varchar(100),
                country char(2) not null references Country(short_code)
            );
            ```