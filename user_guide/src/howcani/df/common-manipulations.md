# 常用操作

与许多其他数据框架库一样，Polars 提供了大量的常用函数来对 Dataframe 进行操作。
熟悉 Dataframes 的用户会发现 Polars 与 `Pandas` 或 `R` 的实现有许多相似之处。

## 添加列

```python
{{#include ../../examples/df_manipulations/add_column.py:4:}}
print(out)
```

```text
{{#include ../../outputs/df_manipulations/add_column.txt}}
```

## 类型转换

这个例子使用的是 Python 数据类型，但我们也可以在 Polars `dtypes`
（如 `pl.Float32`、`pl.Float64`）之间进行转换。

```python
{{#include ../../examples/df_manipulations/casting.py:4:}}
print(out)
```

```text
{{#include ../../outputs/df_manipulations/casting.txt}}
```

## 重命名列

```python
{{#include ../../examples/df_manipulations/rename_column.py}}
```

```text
{{#include ../../outputs/df_manipulations/rename_column.txt}}
```

## 删除列

```python
{{#include ../../examples/df_manipulations/drop_column.py:3:}}
```

```text
{{#include ../../outputs/df_manipulations/drop_column.txt}}
```

## 删除空值

```python
df.drop_nulls()
```

```text
{{#include ../../outputs/df_manipulations/drop_nulls.txt}}
```

## 填充缺失值（NA）

策略:

- `mean`：平均值
- `backward`：上一值
- `min`：最小值
- `max`：最大值

```python
df.fill_none("forward")
```

```text
{{#include ../../outputs/df_manipulations/fill_na.txt}}
```

## 获取所有列

```python
df.columns
```

```text
{{#include ../../outputs/df_manipulations/get_columns.txt}}
```

## 空值计数

```python
df.null_count()
```

```text
{{#include ../../outputs/df_manipulations/null_count.txt}}
```

## 列排序

```python
df.sort("a", reverse=True)
```

```text
{{#include ../../outputs/df_manipulations/sort_columns.txt}}
```

## 转为 NumPy

```python
df.to_numpy()
```

```text
{{#include ../../outputs/df_manipulations/to_numpy.txt}}
```

## 转为 Pandas

```python
df.to_pandas()
```

```text
{{#include ../../outputs/df_manipulations/to_pandas.txt}}
```
