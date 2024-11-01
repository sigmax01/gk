---
title: 数据库:绪论
comments: true
---

## 配套课程

该库的配套课程为[COMP9120](https://www.sydney.edu.au/units/COMP9120).

### 友情链接

- Canvas: [https://canvas.sydney.edu.au/courses/59729](https://canvas.sydney.edu.au/courses/59729)
- Ed Discussion: [https://edstem.org/au/courses/16746/discussion/](https://edstem.org/au/courses/16746/discussion/)
- Modules: [https://canvas.sydney.edu.au/courses/59729/modules](https://canvas.sydney.edu.au/courses/59729/modules)
- Assignments: [https://canvas.sydney.edu.au/courses/59729/assignments](https://canvas.sydney.edu.au/courses/59729/assignments)
- Marks: [https://canvas.sydney.edu.au/courses/59729/grades](https://canvas.sydney.edu.au/courses/59729/grades)
- Quizzes: [https://canvas.sydney.edu.au/courses/59729/quizzes](https://canvas.sydney.edu.au/courses/59729/quizzes)

### 上课地点

- 讲座: [A21.02.200.Wallace Theatre.Wallace Lecture Theatre 200](https://maps.sydney.edu.au/?room=A21.02.200).
- 补习: [F07.06.610-611.Carslaw Building.Carslaw Computer Lab 610-611](https://maps.sydney.edu.au/?room=F07.06.610-611)

### 上课时间

- 讲座: 2024学年第二学期星期四18:00-19:00
- 补习: 2024学年第二学期星期五19:00-20:00

### 联系方式

- Athman Bouguettaya教授, athman.bouguettaya@sydney.edu.au
- Mohammad Masbaul Alam Polash博士, masbaul.polash@sydney.edu.au

### 分数分布

- 期末考试: 50%, 纸笔考试, 2小时
- 大作业1: 16%, 小组作业, 基于给定问题设计一个理论模型并给出相应的SQL实现, n/a
- 大作业2: 16%, 小组作业, 使用数据库开发一个应用程序, 需要有Python方面的基础, n/a
- 小考试: 18%, 纸笔考试, 50分钟

### 截止日期

|作业|截止日期|完成情况|完成日期|备注|
|-|-|-|-|-|
|大作业1|第六周(9月8日)|✅|||
|小考试|第十周|✅|||
|大作业2|第十一周(10月20日)|✅|||
|期末考试|考试周||||

### 惩罚措施

迟交一天作业, 扣除5%该作业的总分(不是得分). 十天之后, 取消成绩.

### 课程内容

|周数| 主题                                                        |
|-|-----------------------------------------------------------|
|第一周| 绪论                                                        |
|第二周| [数据模型](/database/conceptual-model)                        |
|第三周| [关系模型](/database/conceptual-model)                        |
|第四周| [关系代数](/database/relational-algebra)+[SQL](/database/sql) |
|第五周| [完整性约束](/database/integrity-constraints)                  |
|第六周| [高级SQL](/database/advanced-sql)                           |
|第七周| [应用开发](/database/app-dev)                                 |
|第八周| [规范化](/database/normalization)                            |
|第九周| [事务](/database/transaction)                               |
|第十周| [存储与索引](/database/storage-indexing)                       |
|第十一周| [查询处理](/database/query-processing)                        |

### 学习资源

- [Database Management Systems](https://drive.google.com/file/d/1PzsSu6P5BwX91bJHu-9pCh6vikslcuQr/view?usp=sharing)
- [A First Course in Database Systems](https://drive.google.com/file/d/1EwY5MhTM2Q9PtkOMcraBgI5Zt-ps6SYW/view?usp=sharing)
- [Database Systems: An Application-Oriented Approach](https://archive.org/details/databasesystemsa0002kife)

### 考试

题型: 

- 3个MCQ, 6分
- 9个简答题, 44分

重点考察:

- 画ERD
- ERD如何将其转为RM
- 写SQL语句
- 五个范式怎么用, 怎么判断
- 将SQL语句转为关系代数
- 冲突可串行化如何判断, 如何将其转化为串行调度
- 几个loop join算法

### 备注

- 该课程对出席率没有要求
- 所有的课程内容都会发布在[Modules](https://canvas.sydney.edu.au/courses/59729/modules)中
- 每一个小组最多包含3个人, 在补习课上组队, 在Canvas --> People --> Assignment Groups下添加组队信息. 若两周之内没有组队, 则会被随机分配到一个组中. 也可以是不同补习课上的同学组队

## 安装

### Archlinux[^1]

```
sudo pacman -Syu
sudo pacman -S postgresql
sudo -i
passwd postgres
# 输入密码
exit
su - postgres -c "initdb --locale zh_CN.UTF-8 -D '/var/lib/postgres/data'"
sudo systemctl start postgresql.service
sudo mkdir -p /var/lib/pgadmin
sudo mkdir -p /var/log/pgadmin
sudo chown postgres /var/lib/pgadmin
sudo chown postgres /var/log/pgadmin
sudo -iu postgres
mkdir test
cd test
python -m venv .venv
source .venv/bin/activate
pip install pgadmin4
pgadmin4
# 输入邮箱, 密码, 进程启动, 进入提供的URL
# 用户名, 密码为postgres, 以及之前创建用户时使用的密码
```

[^1]: https://www.yuweihung.com/posts/2022/archlinux-install-postgresql/