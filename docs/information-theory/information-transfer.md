---
title: 信息论:信息传递
comments: true
---

## 背景

回顾一下[上节课](/information-theory/information-storage), 我们正在构建一个目标变量动态的模型, 已经考虑了目标变量过去的信息(即存储信息的部分). 那么, 现在引入一个新的"源变量", 假设已经知晓了目标变量过去的信息, 从源变量过去的信息中, 有多少信息能够帮助预测目标变量下一个状态, 这是通过信息传递衡量的.

就拿心跳消息来说吧. 

<figure markdown='1'>
![](https://img.ricolxwz.io/a7f34828dfed10ebf293bb2b0cf2b104.png){ loading=lazy width='200' }
</figure>

左侧是源变量, 右侧是目标变量. 在这种情况下, 目标变量只是简单地复制源变量的消息. 源变量的消息状态的转变符合泊松分布. 将源变量记为$s$, 目标变量记为$t$, 有$t_{n+1}=s_n$.

<figure markdown='1'>
![](https://img.ricolxwz.io/dab1a772c5a6d3dc55345d9dfb1465ea.png){ loading=lazy width='250' }
</figure>

由于$\lambda_1, \lambda_2 << 0.5$, 且$\lambda_1 < \lambda_0$, 所以原变量的状态基本上是$0$.

现在, 你需要建模目标变量, 预测目标变量的下一个状态, 从两个角度出发:

- 根据过去信息做出预测: 你需要根据目标变量过去的信息和你对系统的理解, 对目标的下一个状态做出预测. 并且, 用$1$到$10$来打分记录你的确幸程度✅
- 结合源变量更新预测: 在你基于目标变量的过去状态做出初步预测后, 结合源变量的状态来更新你的预测, 同样用$1$到$10$来打分记录你的确幸程度✅

思考源变量在什么情况下对目标变量的预测最有帮助, 在哪些情况下帮助较少.

## 传递熵

传递熵, Transfer Entropy, TE, 衡量了在已经考虑了目标过程$X$的过去状态$\bm{X}_n^{(k)}=\{X_{n-k+1}, ..., X_{n-1}, X_n\}$的情况下, 源过程$Y$中的观察值$Y_n$能够在多大程度上帮助预测目标过程$X$的下一个状态$X_{n+1}$. 换句话说, TE描述的是在已知目标变量过去状态的条件下, 源变量过去的信息对预测目标变量未来状态所提供的额外帮助.

传递熵的计算公式为$T_{Y\rightarrow X}=\lim_{k\rightarrow \infty}I(Y_n;X_{n+1}|\bm{x}_n^{(k)})$. 或者考虑$k$个目标变量的历史记录$T_{Y\rightarrow X}(k)=I(Y_n;X_{n+1}|\bm{x}_n^{(k)})$. 它还可以表示为$T_{Y\rightarrow X}(k)=<\log_2\frac{p(x_{n+1}|\bm{x}_n^{(k)}, y_n)}{p(x_{n+1}|\bm{x}_n^{(k)})}>$. $t_{Y\rightarrow X}(k)=\log_2\frac{p(x_{n+1}|\bm{x}_n^{(k)}, y_n)}{p(x_{n+1}|\bm{x}_n^{(k)})}$.

### 和存储信息的关系

那么, 如果我们不考虑目标过程$X$的过去状态$\bm{X}_n^{(k)}$, 只考虑源过程的$Y_n$呢? 即$I(Y_n;X_{n+1}|\bm{X}_n^{(k)})$和$I(Y_n;X_{n+1})$的区别在哪里. 首先, 两个都是具有方向性的(?个人看法后者是没有方向性的), 但是前者的条件性使得TE具有动态性. 而且条件化会对互信息的值产生影响:

互信息度量的是两个随机变量之间的总体依赖性, 然而, 这种依赖性可能包含冗余信息, 例如这两个变量通过第三个变量共享的信息, 条件互信息通过引入一个条件变量来量化两个变量在给定第三个变量的情况下的依赖关系, 从而排除了由该条件变量所引入的冗余信息.

在上述的例子中, 可以看到, 目标变量其实有相当一大部分都是由自身之前的状态决定的, 因此$Y_n$提供的信息在相当大的程度上是多余, 而条件互信息更加专注于源状态$Y_n$提供的额外信息. 自身之前的状态就是[存储信息](/information-theory/information-storage/#ais), 通过条件化历史, 能够更清晰地将存储信息排除在传递之外.

因此, 信息传递的计算公式也可以写为$H(X_{n+1})=I(\bm{X}_n^{(k)};X_{n+1})+I(Y_n;X_{n+1}|\bm{X}_n^{(k)})+H(X_{n+1}|\bm{X}_n^{(k)}, Y_n)$. 第一项表示目标变量$X$和自己的过去$\bm{X}_n^{(k)}$与$X_{n+1}$之间的互信息, 这部分是储存的信息. 第二项表示排除了存储信息的影响之后, 源变量$Y$传递到目标变量$X_{n+1}$的信息, 这就是传递熵. 第三项是在考虑了源信息和存储信息之后, 未来状态的剩余不确定性.

TE和存储信息的关系可以用下图来表示:

<figure markdown='1'>
![](https://img.ricolxwz.io/95f22e475af285b2d1cf69de0cec0c87.png){ loading=lazy width='250' }
</figure>

图中, 整个椭圆表示的是总体的互信息量, 表示源变量$Y$和目标变量的过去状态$M$共同对目标未来状态提供的信息. AIS对应的是白色部分, $\{M\}$表示的是目标变量过去的信息, 就是存储信息. 可以看到, 存储信息$\{M\}$是和源变量对于目标变量的贡献$\{Y\}$是有重叠部分的, 即$\{M\}\{Y\}$, 这个重叠部分就是被条件互信息中的条件给消除掉了, 是冗余信息. 

传递熵对应的是整个绿色部分, 可以看到, 它不仅仅包含来自源变量的信息, 还包含源变量和目标变量过去状态共同作用的协同信息$\{MY\}$. 

### 和因果效应的区别

因果效应是关于干预的效果. 意思是, 如果你改变了某个变量, 比如$Y$, 会不会导致另一个变量, 比如$X$发生变化. 这是通过主动干预(如让一组人喝咖啡, 另一组人不喝咖啡, 然后观察他们的睡眠质量变化)来确定因果关系的, 重点在于一个变量的变化是否导致了另一个变量的变化. 信息传递关注的是信息如何流动. 并不需要对系统进行干预, 而是观察两个变量在时间上的变化关系, 看一个变量是否能传递信息给另一个变量.

如下面的这个例子:

<figure markdown='1'>
![](https://img.ricolxwz.io/33fbfbc509e98244e8dd31f7e903cc30.png){ loading=lazy width='280' }
</figure>

过程1中$Y$和$X$的值交替变化, 过程2中$Y$和$X$的值各自独立变化. 因果效应分析会认为过程1中$Y$有可能影响X, 过程2可能没有影响. 但是信息传递模型可能认为这两个过程都没有真正的信息传递, 更多的是参考自己的历史信息, 即存储信息.

---

与存储信息类似, 在计算传递熵的时候也可以加一个[时间延迟](information-theory/information-storage/#set-k), $T_{Y\rightarrow X}(k, \tau_X)=I(Y_n;X_{n+1}|\bm{X}_n^{(k, \tau_X)})$. 同样的, 也可以使用类似的方法[选择合适的"甜蜜点"](information-theory/information-storage/#set-k). 

计算过程为:

1. 历史嵌入: 必须首先进行目标的历史嵌入, 而不是同时嵌入源和目标, 这是为了确保传递熵能够专注于捕捉真正的新信息传递, 并且考虑源和历史的协同作用
2. 源嵌入: 这里我们对刚才的公式做一个扩展, 我们的传递上不仅仅以来源变量当前的值, 与目标变量历史嵌入类似, 我们也有$l$阶源变量目标历史信息, 以及延迟$\tau_Y$, $T_{Y\rightarrow X}(k, l, \tau_X, \tau_Y)=I(\bm{Y}_n^{(l, \tau_Y)}; X_{n+1}|\bm{X}_n^{(k, \tau_X)})$
3. 设置源-目标延迟: 其实刚刚的那个公式还是经过简化的..., 还有一个源-目标延迟可供设置. 这个延迟$u$表示源变量的历史状态和目标变量的未来状态之间的延迟. 例如在某些物理系统或者生物系统中, 某一过程的变化不会立即影响另一个过程, 而是需要经过一段时间. $T_{Y\rightarrow X}(k, l, \tau_X, \tau_Y, u)=I(\bm{Y}_{n+1-u}^{(l, \tau_Y)}; X_{n+1}|\bm{X}_n^{(k, \tau_X)})$

## 条件传递熵

条件传递熵回答了这样一个问题: 在考虑目标变量$X$的过去状态$\bm{X}_n^{(k)}$和另一个过程$X$的观测$Z_n$的情况下, 源变量$Y_n$中有多少信息能够传递给目标变量$X$的未来状态$X_{n+1}$.

其公式为$T_{Y\rightarrow X|Z}=\lim_{k\rightarrow \infty}I(Y_n;X_{n+1}|\bm{X}_n^{(k)}, Z_n)$. 有限嵌入的公式为$T_{Y\rightarrow X|Z}(k)=I(Y_n;X_{n+1}|\bm{X}_n^{(k)}, Z_n)$. 概率表示为$T_{Y \to X | Z}(k) = <\log_2 \frac{p(x_{n+1} \mid x_n^{(k)}, y_n, z_n)}{p(x_{n+1} \mid x_n^{(k)}, z_n)}>$, $t_{Y \to X | Z}(k) = \log_2 \frac{p(x_{n+1} \mid x_n^{(k)}, y_n, z_n)}{p(x_{n+1} \mid x_n^{(k)}, z_n)}$. 同样的, 也可以添加一众延迟等参数...

### 额外条件的影响

引入条件$Z$产生的影响主要有:

- 冗余去除: 如果源变量$Y$和条件变量$Z$之间共享某些信息, 这种冗余信息会被条件化消除
    <figure markdown='1'>
    ![](https://img.ricolxwz.io/ea71b0c1bb9bd1601d1d87a06bf026eb.png){ loading=lazy width='280' }
    </figure>
- 协同效应: 当$Y$和$Z$共同作用影响$X$的时候, 能够捕捉到这种协同信息
    <figure markdown='1'>
    ![](https://img.ricolxwz.io/b0dcb14f8456a3a5d15f59f0198158a0.png){ loading=lazy width='180' }
    </figure>

## 信息回归

当我们考虑目标变量的未来状态$X_{n+1}$的时候, 有两个信源$Y_n$和$Z_n$(后者是选择性的, 可有可无), 再加上历史信息$\bm{X}_n^{(k)}$, 我们能够分解$X_{n+1}$的信息来源. 

<figure markdown='1'>
![](https://img.ricolxwz.io/55d4376cb94e5e341d9ed3382f3b3329.png){ loading=lazy width='500' }
</figure>

其中, 主要的概念有:

- AIS: 存储信息
- Pairwise Transfer Entropy: 两个变量之间的传递熵
- Collective Transfer Entropy: 是从多个来源(如$Y_n$和$Z_n$)共同传递到目标变量的传递熵
- Conditional Transfer Entropy: 是相对于某个条件下的传递熵

可以看到, $H(X_{n+1})$拆分的方式有很多种.