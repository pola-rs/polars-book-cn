# 透视

在 `DataFrame` 中透视一列，并执行下列其中一种聚合。

- first：第一项
- sum：求和
- min：最小值
- max：最大值
- mean：平均值
- median：中位数

透视操作包括一个或多个列的分组（它们将成为新的 y 轴），将被透视的列（它们将成为新的 x 轴）以及一个聚合。

## 数据集

```python
{{#include ../../examples/pivot/dataset.py}}
print(df)
```

```text
{{#include ../../outputs/pivot/dataset.txt}}
```

## 急性

```python
{{#include ../../examples/pivot/eager.py:2:}}
```

## 惰性

惰性操作的 API 中并不包含转置操作，因此想要`惰性地`使用转置，我们可以使用 `map` 来
在惰性计算节点中执行一个急性的自定义函数。

```python
{{#include ../../examples/pivot/lazy.py:2:}}
print(out)
```

```text
{{#include ../../outputs/pivot/lazy.txt}}
```
