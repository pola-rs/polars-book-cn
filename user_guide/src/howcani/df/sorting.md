# 排序

Polars 支持与其他数据框架库类似的排序行为，即按一个或多个列以及多个（不同的）顺序进行排序。

## 数据集

```python
{{#include ../../examples/sorting/dataset.py}}
print(df)
```

```text
{{#include ../../outputs/sorting/dataset.txt}}
```

## 急性

```python
{{#include ../../examples/sorting/eager.py:3:}}
print(out)
```

```text
{{#include ../../outputs/sorting/eager.txt}}
```

## 惰性

```python
{{#include ../../examples/sorting/lazy.py:2:}}
print(out)
```

```text
{{#include ../../outputs/sorting/lazy.txt}}
```
