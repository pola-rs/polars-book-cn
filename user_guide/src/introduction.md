<div style="margin: 30px auto; background-color: white; border-radius: 50%; width: 200px; height: 200px;"><img src="https://raw.githubusercontent.com/pola-rs/polars-static/master/logos/polars-logo-dark.svg" alt="Polars logo" style="width: 168px; height: 168px; padding: 10px 20px;"></div>

# 介绍

这是一个介绍[`Polars` DataFrame library](https://github.com/pola-rs/polars)的指南。它的目标是通过阅读示例并与其他示例进行比较，向您介绍`Polars`解决方案。这里介绍了一些设计选择。该指南还将向您介绍`Polars`的最佳使用。

尽管`Polars`完全是用[`Rust`](https://www.rust-lang.org/)写的（没有运行时开销！）使用 [`Arrow`](https://arrow.apache.org/) -- [原生 `Rust` 实现的arrow2](https://github.com/jorgecarleitao/arrow2) -- 作为它的底基。本指南中的示例主要使用其更高级的语言绑定。高级绑定只作为核心库中实现的功能的简要的包装。

对于 [`Pandas`](https://pandas.pydata.org/) 使用者, 我们的[Python package](https://pypi.org/project/polars/) 提供最简单的方式来启动`Polars`.

## 目标与非目标

`Polars`的目标是提供一个闪电般的`DataFrame`库，利用所有机器上的可用内核。不像dask这样的工具——它试图并行化现有的单线程库，比如`NumPy`和`Pandas`——`Polars`是从头开始编写的，旨在并行化`DataFrame`上的查询。

`Polars`不遗余力地：

- 减少冗余拷贝
- 高效地遍历内存缓存
- 最小化并行中的争用

`Polars`是懒惰和半懒惰的。它可以让你急切地完成大部分工作，就像`Pandas`一样，但是
它还提供了强大的表达式语法，可以在查询引擎中对其进行优化和执行。

在lazy `Polars`中，我们能够对整个查询进行查询优化，进一步提高性能和内存压力。

`Polars`以*逻辑计划*跟踪您的查询。这计划在运行前经过优化和重新排序。当请求结果时，`Polars`将可用的工作分配给使用可用算法的不同*执行者*在渴望产生结果的API中。因为所有人都知道整个查询上下文逻辑计划的优化器和执行者，流程依赖于单独的数据源可以动态并行。

![](https://raw.githubusercontent.com/pola-rs/polars-static/master/docs/api.svg)

### 性能 🚀🚀

Polars的速度非常快，事实上是目前性能最好的解决方案之一。参见h2oai的db基准测试中的结果。下图显示了产生结果的最大数据集。

![](https://www.ritchievink.com/img/post-35-polars-0.15/db-benchmark.png)

### 当前状态

下面是`Polars`能够实现其目标的功能的简明列表：

- [Copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write) (COW) 语义学
  - “自由”克隆（Clone）
  - 便捷的追加（append）
- 没有克隆（clone）的追加（append）
- 面向列的数据存储
  - 无区块管理器（即可预测的性能）
- 缺少用位掩码（bitmask）指示的值
  - NaN和missing不一样
  - 位掩码（bitmask）优化
- 高效算法
- 非常快的IO
  - 它的csv和parquet 阅读器是现存速度最快的阅读器之一
- [查询优化](optimizations/lazy/intro.md)
  - 谓词（Predicate）下推
    - 扫描级过滤
  - 投影下推
    - 扫描级投影
  - 聚合下推
    - 扫描级聚合
  - 简化表达式
  - 物理计划的并行执行
  - 基于基数的分组调度
    - 基于数据基数的分组策略
- SIMD矢量化
- [`NumPy` 通用函数](https://numpy.org/doc/stable/reference/ufuncs.html)

## 致谢

`Polars`的开发是由

[![Xomnia](https://raw.githubusercontent.com/pola-rs/polars-static/master/sponsors/xomnia.png)](https://www.xomnia.com)
