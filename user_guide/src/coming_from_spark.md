# 从 Apache Spark 转化

## 基于列的 API vs. 基于行的 API

`Spark` `DataFrame` 类似于一个行的集合，而 `Polars` `DataFrame` 更接近于一个列的集合。这意味着你可以在 `Polars` 中以 `Spark` 中不可能的方式组合列，因为 `Spark` 保留了每一行中的数据关系。

考虑一下下面这个样本数据集。

```python
import polars as pl

df = pl.DataFrame({
    "foo": ["a", "b", "c", "d", "d"],
    "bar": [1, 2, 3, 4, 5],
})

dfs = spark.createDataFrame(
    [
        ("a", 1),
        ("b", 2),
        ("c", 3),
        ("d", 4),
        ("d", 5),
    ],
    schema=["foo", "bar"],
)
```

### 案例 1: 合并 `head` 与 `sum`

在 `Polars` 中你可以写出下面的语句：

```python
df.select([
    pl.col("foo").sort().head(2),
    pl.col("bar").filter(pl.col("foo") == "d").sum()
])
```

该代码段输出:

```
shape: (2, 2)
┌─────┬─────┐
│ foo ┆ bar │
│ --- ┆ --- │
│ str ┆ i64 │
╞═════╪═════╡
│ a   ┆ 9   │
├╌╌╌╌╌┼╌╌╌╌╌┤
│ b   ┆ 9   │
└─────┴─────┘
```

列 `foo` 和 `bar` 上的表达式是完全独立的。由于 `bar` 上的表达式返回一个单一的值，这个值在 `foo` 表达式输出的每个值中都会重复，但是 `a` 和 `b` 与产生 `9` 没有关系。

要在 `Spark` 中做类似的事情，你需要单独计算总和，并将其作为字面值返回：

```python
from pyspark.sql.functions import col, sum, lit

bar_sum = (
    dfs
    .where(col("foo") == "d")
    .groupBy()
    .agg(sum(col("bar")))
    .take(1)[0][0]
)

(
    dfs
    .orderBy("foo")
    .limit(2)
    .withColumn("bar", lit(bar_sum))
    .show()
)
```

该代码段输出:

```
+---+---+
|foo|bar|
+---+---+
|  a|  9|
|  b|  9|
+---+---+
```

### 案例 2: 合并两个 `head`

在 `Polars` 中你可以在同一个 DataFrame 上结合两个不同的 `head` 表达式，只要它们返回相同数量的值。

```python
df.select([
    pl.col("foo").sort().head(2),
    pl.col("bar").sort(reverse=True).head(2),
])
```

该代码段输出:

```
shape: (3, 2)
┌─────┬─────┐
│ foo ┆ bar │
│ --- ┆ --- │
│ str ┆ i64 │
╞═════╪═════╡
│ a   ┆ 5   │
├╌╌╌╌╌┼╌╌╌╌╌┤
│ b   ┆ 4   │
└─────┴─────┘
```

同样，这里的两个 `head` 表达式是完全独立的，`a` 与 `5` 和 `b` 与 `4` 的配对纯粹是表达式输出的两列并列的结果。

为了在 `Spark` 中完成类似的工作，你需要生成一个人工的 key 使你能够以相同的方式连接这些值。

```python
from pyspark.sql import Window
from pyspark.sql.functions import row_number

foo_dfs = (
    dfs
    .withColumn(
        "rownum",
        row_number().over(Window.orderBy("foo"))
    )
)

bar_dfs = (
    dfs
    .withColumn(
        "rownum",
        row_number().over(Window.orderBy(col("bar").desc()))
    )
)

(
    foo_dfs.alias("foo")
    .join(bar_dfs.alias("bar"), on="rownum")
    .select("foo.foo", "bar.bar")
    .limit(2)
    .show()
)
```

该代码段输出:

```
+---+---+
|foo|bar|
+---+---+
|  a|  5|
|  b|  4|
+---+---+
```
