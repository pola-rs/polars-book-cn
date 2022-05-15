# 入门

## 安装

采用 `pip install` 即可安装 `Polars` 。

```shell
$ pip install polars
```

所有的二进制包都是基于 `Python` v3.6+ 构建的。

## 实例

下面的例子中我们读入并解析一个 CSV 文件，过滤后连接一个 `groupby` 操作：

```python
import polars as pl

df = pl.read_csv("https://j.mp/iriscsv")
print(df.filter(pl.col("sepal_length") > 5)
      .groupby("species")
      .agg(pl.all().sum())
)
```

上面的代码输出如下：

```text
shape: (3, 5)
╭──────────────┬──────────────────┬─────────────────┬──────────────────┬─────────────────╮
│ species      ┆ sepal_length_sum ┆ sepal_width_sum ┆ petal_length_sum ┆ petal_width_sum │
│ ---          ┆ ---              ┆ ---             ┆ ---              ┆ ---             │
│ str          ┆ f64              ┆ f64             ┆ f64              ┆ f64             │
╞══════════════╪══════════════════╪═════════════════╪══════════════════╪═════════════════╡
│ "virginica"  ┆ 324.5            ┆ 146.2           ┆ 273.1            ┆ 99.6            │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ "versicolor" ┆ 281.9            ┆ 131.8           ┆ 202.9            ┆ 63.3            │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│ "setosa"     ┆ 116.9            ┆ 81.7            ┆ 33.2             ┆ 6.1             │
╰──────────────┴──────────────────┴─────────────────┴──────────────────┴─────────────────╯
```

如上所示， `Polars` 可以格式化输出，包括作为表头的列名和数据类型。

## 惰性实例

上面的例子我们也可以采用惰性方式执行：

```python
import polars as pl

print(
    pl.read_csv("https://j.mp/iriscsv")
    .lazy()
    .filter(pl.col("sepal_length") > 5)
    .groupby("species")
    .agg(pl.all().sum())
    .collect()
)
```

如果数据文件保存在本地，我们还可以使用 `scan_csv` 来实现惰性查询。

## 参考

`Python` API 可以参考：[Fix Me](POLARS_PY_REF_GUIDE).

### 惰性 API

惰性 API 会构建一个查询方案。在调用 `LazyFrame.collect()` 或者 `LazyFrame.fetch()` 之前，
`Polars` 不会执行任何操作。这种方式可以让 `Polars` 了解查询的所有操作，并依据这些操作进行优化，
选择最佳的算法执行。

从饥俄执行到惰性执行的改变非常简单，只需要在已有调用基础上添加 `.lazy()` 和 `.collect()` 即可。

正如之前看到的例子一样：

```python
import polars as pl

print(
    pl.read_csv("https://j.mp/iriscsv")
    .lazy()
    .filter(pl.col("sepal_length") > 5)
    .groupby("species")
    .agg(pl.all().sum())
    .collect()
)
```
