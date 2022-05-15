# 窗口函数 🚀🚀

窗口函数是一种强大的表达式。它可以让用户在 `select` 上下文中分组进行类聚。
让我们通过例子看看这是什么意思。首先，我们创建一个数据结构，这个数据包含如下列，分别代表口袋妖怪的一些信息：

`['#',  'Name',  'Type 1',  'Type 2',  'Total',  'HP',  'Attack',  'Defense',  'Sp. Atk',  'Sp. Def',  'Speed',  'Generation',  'Legendary']`

```python
{{#include ../examples/expressions/window_1.py:0:}}
```

```text
{{#include ../outputs/expressions/window_1.txt}}
```

## Groupby 类聚

下面我们看看如何用窗口函数对不同的列分组并且类聚。这样我们可以在一个潮汛中，并行的运行多个分组操作。
类聚的结果会投射会原有的行。因此，窗口函数永远返回一个跟原有 `DataFrame` 一样规格的 `DataFrame`。

注意，我们使用了 `.over("Type 1")` 和 `.over(["Type 1", "Type 2"])`，利用窗口函数我们可以一个
`select` 语境中实现多个分组类聚。

更好的是，计算过的分组会被缓存并且在不同的窗口函数中共享。

```python
{{#include ../examples/expressions/window_2.py:3:}}
```

```text
{{#include ../outputs/expressions/window_2.txt}}
```

## 分组操作

窗口函数不仅仅可以类聚，还可以用来按照组施加自定义函数。例如，如果你想要在某一组中排序，你可以：
`.col("value").sort().over("group")`。

让我们试着过滤一些行：

```python
{{#include ../examples/expressions/window_group_1.py:4:}}
print(filtered)
```

```text
{{#include ../outputs/expressions/window_group_1.txt}}
```

注意到，分组 `Water` 的列 `Type 1` 并不连续，中间有两行 `Grass`。而且，同组中的每一个口袋妖股
被按照 `Speed` 升序排列。不幸的是，这个例子我们希望降序排列，幸运的是，这很简单：

```python
{{#include ../examples/expressions/window_group_2.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/window_group_2.txt}}
```

`Polars` 会追踪每个组的位置，并把相应的表达式映射到适当的行。这个操作可以在一个 select 环境中完成。

窗口函数的强大之处在于：你通常不需要 `groupby -> explode` 组合，而是把逻辑放入一个表达式中。
这也使得 API 更加简洁：

- `groupby` -> 标记类聚的分组，返回一个跟组的个数一致的 `DataFrame`
- `over` -> 标记我们希望对这个分组进行计算，但是不会更改原有 `DataFrame` 的形状

## 窗口表达式的规则

窗口表达式的计算规则如下（假设我们有一个 `pl.Int32` 列）：

```python
# 分组内类聚且广播
# 输出类型: -> Int32
pl.sum("foo").over("groups")

# 组内加和，然后乘以组内的元素
# 输出类型: -> Int32
(pl.col("x").sum() * pl.col("y")).over("groups")

# 组内加和，然后乘以组内的元素
# 并且组内类聚成一个列表
# 输出类型: -> List(Int32)
(pl.col("x").sum() * pl.col("y")).list().over("groups")

# 注意这里需要一个显式的 `list` 调用
# 组内加和，然后乘以组内的元素
# 并且组内类聚成一个列表
# list() 会展开

# 如果组内是有序的，这是最快的操作方法：
(pl.col("x").sum() * pl.col("y")).list().over("groups").flatten()
```

## More examples

更多练习，下面是一些窗口函数：

- 按照 `Type` 给所有口袋妖怪排序
- 选择每组前三个妖怪
- 每组按照速度排序，并选择前三作为 `"fastest/group"`
- 每组按照攻击排序，并选择前三作为 `"strongest/group"`
- 每组按照名字排序，并选择前三作为 `"sorted_by_alphabet"`

```python
{{#include ../examples/expressions/window_3.py:3:}}
```

```text
{{#include ../outputs/expressions/window_3.txt}}
```

## 展开窗口函数

就像刚刚的例子，如果你的窗口函数返回一个 `list`：

`pl.col("Name").sort_by(pl.col("Speed")).head(3).list().over("Type 1")`

这样可以，但是这样会返回一个类型为 `List` 的列，这可能不是我们想要的，而且会增加内存使用。

这是我们可以采用 `flatten`。这个函数会把一个 2D 列表转换成 1D，然后把列投射到我们的 `DataFrame`。
这个操作非常快，因为 reshape 基本没有成本，给原有 `DataFrame` 增加列也非常快，因为我们不需要
一般窗口函数的联合（Join）操作。

但是，想要正确的使用这个操作，我们要保证用于 `over` 的列是有序的。
