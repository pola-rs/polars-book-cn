# 连接

类似于其他数据框架库，Polars 支持一系列连接操作。

- 在单个或多个列上进行连接
- 左连接
- 内连接
- 外连接

## 数据集

```python
{{#include ../../examples/join/dataset.py}}
print(df_a)
```

```text
{{#include ../../outputs/join/dataset_a.txt}}
```

```python
print(df_b)
```

```text
{{#include ../../outputs/join/dataset_b.txt}}
```

## 急性

```python
{{#include ../../examples/join/eager.py:2:}}
print(out)
```

```text
{{#include ../../outputs/join/eager.txt}}
```

## 惰性

```python
{{#include ../../examples/join/lazy.py:2:}}
print(out)
```

```text
{{#include ../../outputs/join/lazy.txt}}
```
