---
title: 信息论:绪论
comments: true
---

## 配套课程

该库的配套课程为[CSYS5030](https://www.sydney.edu.au/units/CSYS5030/2024-S2C-NE-CC).

### 友情链接

- Canvas: [https://canvas.sydney.edu.au/courses/59732](https://canvas.sydney.edu.au/courses/59732)
- Discussions: [https://canvas.sydney.edu.au/courses/59732/discussion_topics](https://canvas.sydney.edu.au/courses/59732/discussion_topics)
- Modules: [https://canvas.sydney.edu.au/courses/59732/modules](https://canvas.sydney.edu.au/courses/59732/modules)
- Assignments: [https://canvas.sydney.edu.au/courses/59732/assignments](https://canvas.sydney.edu.au/courses/59732/assignments)
- Marks: [https://canvas.sydney.edu.au/courses/59732/grades](https://canvas.sydney.edu.au/courses/59732/grades)

### 上课地点

[H69.01.151.Business School Codrington Building.BS Codrington Computer Lab (1) 151](https://maps.sydney.edu.au/?room=H69.01.151).

### 上课时间

2024学年第二学期星期三18:00-21:00.

### 联系方式

- Joseph Lizier教授, joseph.lizier@sydney.edu.au
- Jaime Ruiz Serra, jaime.ruizserra@sydney.edu.au

### 分数分布

- 大作业1: 35%, 项目报告, 2000字
- 大作业2: 20%, 计算和简短问题回答, n/a
- 小评估: 15%, 总结和关键词分析, 500字
- 汇报: 30%, 视频汇报, 10分钟+QA

### 截止日期

|作业|截止日期|完成情况|完成日期|备注|
|-|-|-|-|-|
|大作业2|第五周(9月1日)|✅|9月1日||
|小评估|第七周(9月15日)|✅|-||
|汇报|第12周(10月27日)|✅|||
|大作业1|考试周(11月11日)|✅|||

### 惩罚措施
 
没有特殊情况不接受迟交小评估和汇报, 所有的作业若因为特殊情况迟交的话应该重做. 

### 课程内容

|周数|主题|
|-|-|
|第一周|[不确定性和熵](/information-theory/uncertainty-and-entropy)|
|第二周|[不确定性和熵](/information-theory/uncertainty-and-entropy)|
|第三周|[什么是信息](/information-theory/what-is-information)|
|第四周|[什么是信息](/information-theory/what-is-information)|
|第五周|[JIDT](/information-theory/jidt)|
|第六周|[估计器](/information-theory/estimator)|
|第七周|[统计显著性](/information-theory/statistical-significance)|
|第八周|[自组织](/information-theory/self-organisation)|
|第九周|[信息处理](/information-theory/information-processing)|
|第十周|[信息存储](/information-theory/information-storage)|
|第十一周|[信息传递](/information-theory/information-transfer)|
|第十二周|[有效网络推断](/information-theory/effective-network-inference)|

### 备注

- 这是一个翻转课堂模式. 在参加研讨会之前, 需要完成预习工作, 包括阅读指定的材料, 观看视频讲座, 并至少阅读各种教程任务. 研讨会的主要目的是帮助学生解决问题, 解答对讲座材料的疑问, 并在有时间的前提下深入讨论解释
- 可以选择使用Matlab或者Python来完成教程任务. 会根据大多数人的选择来演示相应的工具. 如果选择是少数人使用的工具, 不用担心, 教师团队会提供两种工具的解决方案. 教室里的电脑支持这两种工具, 学生也可以自己携带笔记本电脑, 以确保在同一环境下进行操作

## 总览 

### 概念

#### 复杂系统

- 有序系统: 其行为是可以预测的, 具有较低的不确定性; 由于状态变化的可能性较少, 因此信息量较低. 系统中的大多数状态都是高概率的常见状态. 如晶体结构, 简单机械装置等
- 无序系统: 其行为是不可预测的, 且有较高的不确定性; 由于状态变化的可能性多且复杂, 因此信息量较高. 系统中的大多数状态都是均匀分布的, 没有明显的高概率状态. 如气体分子的运动, 股市波动等

#### 边缘混沌

边缘混沌是有序和无序系统之间的临界状态, 在这个状态下, 系统即具有一定的只需, 又有足够的灵活性来适应变化, 容易产生低概率的, 信息量大的事件.

#### 低概率状态

低概率状态在系统中出现的概率很低, 但是携带大量信息. 由于这些状态的出现是非常罕见和意外的, 因此信息量较高. 他们在有序系统和无序系统中都有可能出现. 如极端天气事件, 金融市场中的黑天鹅事件等. 

#### 自组织

自组织指在没有外部控制的情况下, 随着时间的推移, 系统内部秩序的增加. 

#### 涌现

涌现指随着规模的增加, 系统内部秩序的增加.

### 复杂系统与信息之间的关系

???+ quote "引用"

    "Although they (complex adpative systems) differ widely in their physical attributes, they resemble one another in the way they handle information. That common feature is perhaps the best starting point for exploring how they operate." --- Murray Gell-Mann

尽管复杂系统在具体表现形式上可能千差万别, 如生物系统, 生态系统, 社会系统等. 但它们在信息处理方面具有很多的共性. 系统通过接收, 传递和处理信息来适应环境变化, 进行自我调整和优化. 为了量化和分析这些概念, 信息论提供了有力的工具和方法. 