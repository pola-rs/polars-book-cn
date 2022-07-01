# 投影下推

> `投影下推`章节正在构建中

我们来把上一章节中的查询与在 Runescape （一款游戏）数据中进行 *FILTER* 操作的结果结合起来，
来找出以字母 `a` 开头且玩过 Runescape 的流行 Reddit 用户名。相信你一定也会对此感兴趣的！

你可以构建类似于以下的查询：

```python
{{#include ../../examples/projection_pushdown/snippet.py}}
```

这将产出以下 DataFrame：

```text
{{#include ../../outputs/projection_pushdown/output.txt}}
```

## 更近一步

让我们再来看看查询计划。

```python
dataset.show_graph(optimized=False)
```

![](./../outputs/projection_pushdown/graph.png)

现在，我们关注的是用 `π` 表示的投影。第一个节点上显示着 π 3/6，这意味着我们从 `DataFrame`
的 6 列中选出了其中的 3 列。在 csv 读取结果中，我们可以看到通配符 `π */6` 和 `π */1`，
这意味着我们选中了 Reddit 数据集中的全部 6 列，以及对应的 Runescape 数据集中唯一的一列。

但是，这样的查询性能并不理想 —— 我们选中了两个数据集的所有列，却只显示了关联 (join) 后的 3 列。
这意味着一些参与关联计算的列实际上是可以被忽略的。类似的，在读取 csv 时解析了一些列，而它们在最后是被白白丢弃掉的。
当我们要处理的 `DataFrame` 中有大量的列时，所做的这种冗余工作量可能是非常可观的。

### 更优查询方案

让我们看看 `Polars` 是如何优化这个查询的。

```python
dataset.show_graph(optimized=True)
```

![](./../outputs/projection_pushdown/graph-optimized.png)

关联 (join) 操作中的投影被下推至 csv 读取的这一步。这意味着查询优化降低了读取数据以及关联操作这二者的开销。

## 性能

让我们为优化前后的结果进行计时。

**优化前**，即 `predicate_pushdown=False` 且 `projection_pushdown=False`。

```text
real    0m3,273s
user    0m9,284s
sys    0m1,081s
```

**优化后**，即将 `predicate_pushdown` 与 `projection_pushdown` 均设置为 `True`。

```text
real    0m1,732s
user    0m7,581s
sys    0m0,783s
```

可以看到，这一简单的优化使得我们节省了将近一半的查询时间！在现实应用中，业务数据通常保存了大量列，
我们预期这使得优化前后的过滤缺失数据、进行复杂的分组操作、关联操作等的性能差异会变得更大。
