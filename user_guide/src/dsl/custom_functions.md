# 自定义函数

现在你应该相信，polar表达式是如此的强大和灵活，以至于对自定义python函数的需求比你在其他库中可能需要的要少得多。

尽管如此，你仍然需要有能力将表达式传递给第三方库，或者将你的黑匣子函数应用于polar数据。

为此，我们提供了以下几种表达式：

- `map`
- `apply`

## map

在操作方式上和最终向用户传递的数据上，`map`和`apply`函数有重要的区别。

`map`函数将表达式所支持的`Series`数据原封不动的传递。

`map`函数在`select`和`groupby`中遵循相同的规则，这将意味着`Series`代表`DataFrame`中的一个列。注意，在`groupby`情况下，该列还没有被分组！

`map`函数的用法是将表达式中的`Series`传递给第三方库。下面我们展示了如何使用`map`将一个表达式列传递给神经网络模型。

```python
df.with_column([
    pl.col("features").map(lambda s: MyNeuralNetwork.forward(s.to_numpy())).alias("activations")
])
```

在`groupby`中，`map`的使用情况很有限。它们只用于性能方面，但很容易导致不正确的结果。让我们来解释一下原因。

```python
df = pl.DataFrame(
    {
        "keys": ["a", "a", "b"],
        "values": [10, 7, 1],
    }
)

out = df.groupby("keys", maintain_order=True).agg(
    [
        pl.col("values").map(lambda s: s.shift()).alias("shift_map"),
        pl.col("values").shift().alias("shift_expression"),
    ]
)
print(df)
shape: (3, 2)
┌──────┬────────┐
│ keys ┆ values │
│ ---  ┆ ---    │
│ str  ┆ i64    │
╞══════╪════════╡
│ a    ┆ 10     │
├╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤
│ a    ┆ 7      │
├╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤
│ b    ┆ 1      │
└──────┴────────┘
```

在上面的片段中，我们按`"keys"`列分组。这意味着我们有以下几个组。

```c
"a" -> [10, 7]
"b" -> [1]
```

如果我们再向右应用一个`shift`操作，我们就会发现。

```c
"a" -> [null, 10]
"b" -> [null]
```

现在，让我们打印一下得到的结果：

```python
print(out)
shape: (2, 3)
┌──────┬────────────┬──────────────────┐
│ keys ┆ shift_map  ┆ shift_expression │
│ ---  ┆ ---        ┆ ---              │
│ str  ┆ list[i64]  ┆ list[i64]        │
╞══════╪════════════╪══════════════════╡
│ a    ┆ [null, 10] ┆ [null, 10]       │
├╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ b    ┆ [7]        ┆ [null]           │
└──────┴────────────┴──────────────────┘
```

😯.. 很明显，我们得到了一个错误答案。`"b"`组甚至从`"a"`组拿到了一个值7😵.

这是一个可怕的错误，因为`map`在我们聚合之前就应用了这个函数！这意味着整个列`[10, 7, 1]`先向右移向到了`[null, 10, 7]`，然后再被聚合。

所以我们的建议是，除非你知道你需要使用`map`并且知道你在做什么，否则永远不要在`groupby`时使用`map`。

## apply

幸运的是，我们可以用`apply`来解决之前的例子。`apply`可以对该操作的最小的逻辑元素起作用。

这就意味着:

- `select`-> 单个元素
- `groupby`-> 单个分组

因此，我们可以用`apply`来解决我们上述的问题：

```python
out = df.groupby("keys", maintain_order=True).agg(
    [
        pl.col("values").apply(lambda s: s.shift()).alias("shift_map"),
        pl.col("values").shift().alias("shift_expression"),
    ]
)
print(out)
shape: (2, 3)
┌──────┬────────────┬──────────────────┐
│ keys ┆ shift_map  ┆ shift_expression │
│ ---  ┆ ---        ┆ ---              │
│ str  ┆ list[i64]  ┆ list[i64]        │
╞══════╪════════════╪══════════════════╡
│ a    ┆ [null, 10] ┆ [null, 10]       │
├╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ b    ┆ [null]     ┆ [null]           │
└──────┴────────────┴──────────────────┘
```

可以看到，我们得到了正确的结果! 🎉

## `select`中的`apply`

在`select`中，`apply`表达式将列的元素传递给python函数。

*注意，你现在正在运行Python，这将会很慢。*

让我们通过一些例子来看看会发生什么。我们将继续使用我们在本节开始时定义的`DataFrame`，并展示一个使用`apply`函数的例子和一个使用表达式API实现相同目标的反例。

### 添加一个计数器

在这个例子中，我们创建了一个全局的 `counter` (计数器)，然后在每处理一个元素时将整数 `1` 添加到全局状态中。每个迭代的增量结果将被添加到元素值中。

```python
counter = 0


def add_counter(val: int) -> int:
    global counter
    counter += 1
    return counter + val


out = df.select(
    [
        pl.col("values").apply(add_counter).alias("solution_apply"),
        (pl.col("values") + pl.arange(1, pl.count() + 1)).alias("solution_expr"),
    ]
)
print(out)
shape: (3, 2)
┌────────────────┬───────────────┐
│ solution_apply ┆ solution_expr │
│ ---            ┆ ---           │
│ i64            ┆ i64           │
╞════════════════╪═══════════════╡
│ 11             ┆ 11            │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ 9              ┆ 9             │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ 4              ┆ 4             │
└────────────────┴───────────────┘
```

### 合并多列值

如果我们想在一次`apply`函数调用中访问不同列的值，我们可以创建`struct`数据类型。这种数据类型将这些列作为字段收集在`struct`中。因此，如果我们从列`"keys"`和`"values"`中创建一个`struct`，我们会得到以下结构元素。

```python
[
    {"keys": "a", "values": 10},
    {"keys": "a", "values": 7},
    {"keys": "b", "values": 1},
]
```

这些将作为`dict`传递给调用的Python函数，因此可以通过`field: str`进行索引。

```python
out = df.select(
    [
        pl.struct(["keys", "values"]).apply(lambda x: len(x["keys"]) + x["values"]).alias("solution_apply"),
        (pl.col("keys").str.lengths() + pl.col("values")).alias("solution_expr"),
    ]
)
print(out)
shape: (3, 2)
┌────────────────┬───────────────┐
│ solution_apply ┆ solution_expr │
│ ---            ┆ ---           │
│ i64            ┆ i64           │
╞════════════════╪═══════════════╡
│ 11             ┆ 11            │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ 8              ┆ 8             │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ 2              ┆ 2             │
└────────────────┴───────────────┘
```

### 返回类型

自定义Python函数对polar而言是黑箱。我们真的不知道你在做什么黑科技，所以我们不得不推断并尽力去理解你的意思。

数据类型是自动推断出来的。我们通过等待第一个非空值来做到这一点。这个值将被用来确定`Series`的类型。

python类型与polars数据类型的映射如下：

- `int`->`Int64`
- `float`->`Float64`
- `bool`->`Boolean`
- `str`->`Utf8`
- `list[tp]`->`List[tp]`(其中内部类型的推断规则相同)
- `dict[str, [tp]]`->`struct`
- `Any`->`object`(在任何时候都要防止这种情况)

作为一个用户，我们希望您能了解我们的工作，以便能更好地利用自定义函数。
