# 过滤

## 急性

Polars 的急性过滤操作与 `Pandas` 中的非常相似。

```python
{{#include ../../examples/filter/eager.py}}
```

或者用下面更符合 `Polars` 习惯的方式：

```python
df.filter(pl.col("a") > 2)
```

## 惰性

惰性过滤操作通常使用以下表达：

```python
{{#include ../../examples/filter/lazy.py:2:}}
```

两者的结果都是：

```text
{{#include ../../outputs/filter/filter.txt}}
```
