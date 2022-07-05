# 重塑

重塑操作将一个宽格式的 DataFrame 逆透视为长格式。

## 数据集

```python
{{#include ../../examples/melt/dataset.py}}
print(df)
```

```text
{{#include ../../outputs/melt/dataset.txt}}
```

## 急性 + 惰性

`急性` 与 `惰性` 操作的 API 相同。

```python
{{#include ../../examples/melt/eager.py:3:}}
print(out)
```

```text
{{#include ../../outputs/melt/eager.txt}}
```
