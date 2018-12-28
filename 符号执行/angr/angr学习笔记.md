## angr学习笔记


#####  angr采用广度优先搜索算法

##### Angr is a symbolic execution engine*.
It can:

* Step through binaries (and follow any branch)
* Search for a program state that meets a given criteria
* Solve for symbolic variables given path (and other) constraints


##### Angr中的执行路径的节点由'SimState'对象表示。 顾名思义，它存储程序的状态，以及以前状态的历史。将这些SimStates链接在一起会创建一条路径。

### 1. 如何在angr中表示一组执行路径，以及如何构建？

Angr在`simulation manager`对象中存储和处理给定程序的一组可能路径。

`simulation manager`提供逐步执行程序以生成可能的路径/状态的功能。

1. Angr在您指示它启动的任何地方启动程序（这是第一个活动状态）
2. 在每个(active state)活动（未终止）状态下执行指令(excute instructions)，直到我们到达分支点或状态终止
3. 在每个分支点，将状态拆分为多个状态(split the state)，并将它们添加到活动状态集
4. 重复步骤2..4直到找到我们想要的或所有状态终止(all state terminate)

##### p36 如何解决路径爆炸的问题

##### p39 如何确定哪些路径会导致失败的状态

一些启发是 算法 ，接下来会介绍一个叫做 Veritesting 的算法。（ps：目前他们应该是没有什么好的方法）

### 总结：Algorithm for Find and Avoid

* 加载二进制文件
* 指定起点（starting point）并创建模拟管理器（simulation manager）