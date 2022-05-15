# 表达式上下文

表达式几乎可以在任何地方使用，但是表达式需要一个上下文，这些上下文包括：

- 选择: `df.select([..])`
- 分组集合: `df.groupby(..).agg([..])`
- hstack 或者增加列: `df.with_columns([..])`

## 语法糖

需要上下文的主要原因是：即使实在饥饿模式中，你也在使用 Polars 的惰性API。
比如如下代码实例：

```python
df.groupby("foo").agg([pl.col("bar").sum()])
```

去掉语法糖后：

```python
(df.lazy().groupby("foo").agg([pl.col("bar").sum()])).collect()
```

这种设计可以让 Polars 把表达式推送给查询引擎，进行一些优化和缓存操作。

## `select` 上下文

在 `select` 上下文中，选择操作是按照列进行的。在选择向下文的表达式必须要返回 `Series` 并且这些 `Series` 需要有相同的长度或者长度为1。

一个长度为 1 的 `Series` 会被广匹配 `DataFrame` 的高度。
注意，`select` 可能会返回一个新的列，这个列可能是一些聚合的结果、一些表达式的组合或者字符串。

#### 选择上下文

```python
{{#include ../examples/expressions/select_context_2.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/select_context_2.txt}}
```

**添加列**

采用 `with_columns` 给 `DataFrame` 增加列同样也是选择上下文。

```python
{{#include ../examples/expressions/with_column_context_1.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/wc_context_1.txt}}
```

## Groupby 上下文

在 `groupby` 上下文中的表达式主要作用域分组上，因此他们会返回任意长度（每个组可能有不同数量的成员）。

```python
{{#include ../examples/expressions/agg_context_1.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/agg_context_1.txt}}
```

除了标准的 `groupby`，还有 `groupby_dynamic` 和 `groupby_rolling` 也属于 Groupby 上下文。
