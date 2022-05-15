# Polars 表达式

下面是一个表达式：

`pl.col("foo").sort().head(2)`

这个表达式的意思是：

1. 选择 `foo` 列
1. 给 `foo` 排序
1. 然后提排序后的前两个值

表达式的强大之处在于：每一个表达式都会生成一个新的表达式，他们可以被串在一起。
你也可以把多个表达式放入一个 `Polars` 的执行上下文中。

比如，下面我们通过 `df.select` 将两个表达式放在同一个执行上下文中：

```python
df.select([
    pl.col("foo").sort().head(2),
    pl.col("bar").filter(pl.col("foo") == 1).sum()
])
```

这里的两个表达式是并行执行的，这就意味着 `Polars` 表达式可以**尴尬并行**（即无通讯并行）。
值得注意的是，每一个表达式的执行可能同时存在更多的并行。

## 表达式举例

这一小节我们通过例子了解表达式。首先，创建一个数据集：

```python
{{#include ../examples/expressions/dataset.py}}
print(df)
```

```text
{{#include ../outputs/expressions/dataset.txt}}
```

你可以通过表达式做很多事情，他们的表达能力很强以至于很多时候你有多种不同的方法实现同一个计算。
为了更好的理解表达式，让我们看更多的例子。

### 计算唯一值

我们可以计算一个列中唯一值。注意这里我们采用了两种不同的方法计算同一个结果。为了避免重复列名称，
我们使用 `alias` 即别名表达式来重命名表达式。

```python
{{#include ../examples/expressions/expressions_examples_1.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/example_1.txt}}
```

### 不同的聚合操作

我们可以完成不同的聚合操作，下面是一些例子，当然还有更多操作比如：`median`, `mean`, `first`
等等。

```python
{{#include ../examples/expressions/expressions_examples_2.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/example_2.txt}}
```

### 过滤和条件选择

当然，我们可以做一些复杂的事情，比如下面的例子中我们计算所有以 `am` 结尾的名字。

```python
{{#include ../examples/expressions/expressions_examples_3.py:4:}}
print(df)
```

```text
{{#include ../outputs/expressions/example_3.txt}}
```

### 二元函数和修改

下面的实例中，用一个条件语句创建一个表达式，我们使用 `when -> then -> otherwise` 的模式。
`when` 函数需要一个谓词表达式 (Predicate expression，因此返回一个布尔类型的 `Series`) 。
`then` 函数需要传入当谓词表达式为真时执行的表达式，而 `otherwise` 函数需要传入谓词表达式为
假的表达式。

你可以传入任何表达式，包括简单的`pl.col("foo")`, `pl.lit(3)`, `pl.lit("bar")`等等。

最终，我们把结果与一个 `sum` 表达式相乘。

```python
{{#include ../examples/expressions/expressions_examples_4.py:4:}}
print(df)
```

```text
{{#include ../outputs/expressions/example_4.txt}}
```

### 窗口表达式

一个 polars 表达式可以隐式地进行 GROUPBY（分组）、AGGREGATION（聚合） 以及 JOIN（联合） 操作。
在下面的例子中，使用`over`函数，我们通过 `group` 进行分组，在 `random` 列执行聚合加法。在下一个表达式中，
通过 `names` 进行分组，在 `random` 列执行聚合列表操作。
这些窗口函数还可以与其他表达式组合形成一个高效计算分组统计指标计算方法。
更多的分组函数[参考这里](POLARS_PY_REF_GUIDE/expression.html#aggregation)。

```python
{{#include ../examples/expressions/window.py:4:}}
print(df)
```

```text
{{#include ../outputs/expressions/window_0.txt}}
```

## 结论

这里我们看到的表达式仅仅是冰山一角。`Polars` 提供了很多表达式，而且他们可以通过多种方式组合。

本篇文档是一个表达式的简介，帮助用户稍微了解如何使用表达式。下一章中我们会讨论在哪些场景
中可以使用表达式。在接下来的章节中，我们还会介绍如何在不同的 `groupby` 场景中使用表达式，并
确保 `Polars` 可以并行执行计算。
