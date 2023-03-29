# 聚合

> 本页还在施工中。。。。

## 多线程

处理表状数据最高效的方式就是通过“分割-处理-组合”的方式并行地进行。这样的操作正是 `Polars` 的
分组操作的核心，也是 `Polars` 如此高效的秘密。特别指出，分割和处理都是多线程执行的。

下面的例子展示了分组操作的流程：

![](https://raw.githubusercontent.com/pola-rs/polars-static/master/docs/split-apply-combine.svg)

对于分割阶段的哈希操作，`Polars` 使用了无锁多线程方式，如下图所示：

![](https://raw.githubusercontent.com/pola-rs/polars-static/master/docs/lock-free-hash.svg)

这样的并行操作可以让分组和联合操作非常非常高效。

> 更多解释参考 [这篇博客](https://www.ritchievink.com/blog/2021/02/28/i-wrote-one-of-the-fastest-dataframe-libraries/)

## 不要“杀死”并行

众所周知，`Python` 慢、水平拓展不好。除了因为是解释型语言，Python 还收到全局解释器锁，GIL。
这就意味着，如果你传入一个 `lambda` 或者 `Python` 自定义函数，`Polars` 速度会被限制，即
无法使用多核进行并行计算。

这是个很糟糕的情况，特别我们在做 `.groupby` 的时候会经常传入 `lambda` 函数。虽然 `Polars`
支持这种操作，但是请注意 Python 的限制，特别是解释器和GIL。

为了解决这个问题，`Polars` 实现了一种非常强大的语法，在其延迟执行API和即时执行API上都有定义。

## Polars Expressions

刚才我们提到自定义 Python 函数会损伤并行能力，`Polars` 提供了惰性 API 来应对这种情况。接下来
我们看看这是什么意思。

我们可以从这个数据集开始：[US congress dataset](https://github.com/unitedstates/congress-legislators).

```python
{{#include ../examples/groupby_dsl/snippet1.py}}
```

#### 基本聚合操作

你可以轻松地把多个聚合表达式放在一个 `list` 里面，并没有数量限制，你可以任意组合你放入任何数量的表达式。
下面这段代码中我们做如下聚合操作：

对于每一个 `first_name` 分组：

- 统计每组的行数：
  - 短版：`pl.count("party")`
  - 长版：`pl.col("party").count()`
- 把每组的性别放入一个列表:
  - 长版： `pl.col("gender").list()`
- 找到每组的第一个 `last_name`：
  - 短版: `pl.first("last_name")`
  - 长版: `pl.col("last_name").first()`

除了聚合，我们还立即对结果进行排序，并取其中前5条记录，这样我们能更好地从宏观角度理解这组数据的特征。

```python
{{#include ../examples/groupby_dsl/snippet1.py}}
```

```text
{{#include ../outputs/groupby_dsl/output1.txt}}
```

#### 条件

简单吧！我们加点料！假设我们想要知道对于每个 `state` 有多少 `Pro` 和 `Anti`。我们可以
不用 `lambda` 而直接查询。

```python
{{#include ../examples/groupby_dsl/snippet2.py}}
```

```text
{{#include ../outputs/groupby_dsl/output2.txt}}
```

类似的，我们可以通过多层聚合实现，但是这不利于我显摆这些很酷的特征😉！

```python
{{#include ../examples/groupby_dsl/snippet3.py}}
```

```text
{{#include ../outputs/groupby_dsl/output3.txt}}
```

#### 过滤

我们也可以过滤分组。假设我们想要计算每组的均值，但是我们不希望计算所有值的均值，我们也不希望直接
从 `DataFrame` 过滤，因为我们后需还需要那些行做其他操作。

下面的例子说明我们是如何做到的。注意，我们可以写明 `Python` 的自定义函数，这些函数没有什么
运行时开销。因为这些函数返回了 `Polars` 表达式，我们并没在运行时让 `Series` 调用自动函数。

```python
{{#include ../examples/groupby_dsl/snippet4.py}}
```

```text
{{#include ../outputs/groupby_dsl/output4.txt}}
```

#### 排序

我们经常把一个 `DataFrame` 排序为了在分组操作的时候保持某种顺序。假设我们我们希望知道
每个 `state` 政治家的名字，并按照年龄排序。我们可以用 `sort` 和 `groupby`：

```python
{{#include ../examples/groupby_dsl/snippet5.py}}
```

```text
{{#include ../outputs/groupby_dsl/output5.txt}}
```

但是，**如果**我们想把名字也按照字母排序，上面的代码就不行了。
幸运的是，我们可以在 `groupby` 上下文中进行排序，与 `DataFrame` 无关。

```python
{{#include ../examples/groupby_dsl/snippet6.py}}
```

```text
{{#include ../outputs/groupby_dsl/output6.txt}}
```

我们甚至可以在 `groupby` 上下文中增加另一个列，并且按照男女排序：
`pl.col("gender").sort_by("first_name").first().alias("gender")`

```python
{{#include ../examples/groupby_dsl/snippet7.py}}
```

```text
{{#include ../outputs/groupby_dsl/output7.txt}}
```

### 结论

上面的例子中我们知道通过组合表达式可以完成复杂的查询。而且，我们避免了使用自定义 `Python` 函数
带来的性能损失 （解释器和 GIL）。

如果这里少了哪类表达式，清在这里开一个 Issue：
[feature request](https://github.com/pola-rs/polars/issues/new/choose)!
