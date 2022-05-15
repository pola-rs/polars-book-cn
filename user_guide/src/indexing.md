# 索引

`Polars` `DataFrame`没有索引，因此索引行为可以是一致的，而不需要  `df.loc`,
`df.iloc`, or a `df.at` 操作。

规则如下（取决于值的数据类型）:

- **数值型**

  - axis 0: 行（row）
  - axis 1: 列（column）

- **数值型 + 字符串**

  - axis 0: 行（这里只接收数字)
  - axis 1: 列（接受数字+字符串值）

- **仅字符串**

  - axis 0: 列（column）
  - axis 1: 报错（error）

- **表达式**

  _所有表达式求值都是并行执行的_

  - axis 0: 列（column）
  - axis 1: 列（column）
  - ..
  - axis n: 列（column）

## 与Pandas的对比

| pandas                                                   | polars                    |
| -------------------------------------------------------- | ------------------------- |
| 选择列<br> `df.iloc[2]`                                     | `df[2, :]`                |
| 按索引选择几行<br> `df.iloc[[2, 5, 6]]`                         | `df[[2, 5, 6], :]`        |
| 选择行的切片<br> `df.iloc[2:6]`                                | `df[2:6, :]`              |
| 使用布尔掩码（boolean mask）选择行<br> `df.iloc[True, True, False]` | `df[[True, True, False]]` |
| 按谓词（predicate）条件选择行<br> `df.loc[df["A"] > 3]`            | `df[df["A"] > 3]`         |
| 选择列的切片<br> `df.iloc[:, 1:3]`                             | `df[:, 1:3]`              |
| 按字符串顺序选择列的切片<br> `df.loc[:, "A":"Z"]`                    | `df[:, "A":"Z"]`          |
| 选择单个值（标量）<br> `df.loc[2, "A"]`                           | `df[2, "A"]`              |
| 选择单个值（标量）<br> `df.iloc[2, 1]`                            | `df[2, 1]`                |
| 选择单个值（Series或DataFrame）<br> `df.loc[2, ["A"]]`           | `df[2, ["A"]]`            |
| 选择单个值 (Series或DataFrame)<br> `df.iloc[2, [1]]`           | `df[2, [1]]`              |

## 表达式

表达式也可以用于索引（它是`df.select`的语法糖）。

这可以用来做一些很有别致的选择。

```python
df[[
    pl.col("A").head(5),  # 从“A”的首部开始获取
    pl.col("B").tail(5).reverse(), # 以逆序的方式获取“B”的后部
    pl.col("B").filter(pl.col("B") > 5).head(5), # 首先得到满足谓词的“B”
    pl.sum("A").over("B").head(5) # 获取“A”在“B”组上的总和，并返回前5个
```
