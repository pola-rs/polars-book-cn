# 条件应用

要修改一个 `Series` 或 `DataFrame` 中的一列，需要以下两步。

1. 基于一些谓词创建一个 `boolean` 掩码
1. 替换掉掩码评估为 `True` 的值
1. （仅当惰性操作时） 定义掩码评估为 `False` 的值

## 数据集

```python
{{#include ../../examples/conditionally_apply/dataset.py}}
df.head()
```

```text
{{#include ../../outputs/conditionally_apply/dataset.txt}}
```

我们可以使用 `.when()`/`.then()`/`.otherwise()` 表达式。

- `when` - 接受一个谓词表达式
- `then` - 当 `谓词 == True` 时使用的表达式
- `otherwise` - 当 `谓词 == False` 时使用的表达式

请参见以下例子。

```python
{{#include ../../examples/conditionally_apply/lazy.py:4:}}
print(df)
```

```text
{{#include ../../outputs/conditionally_apply/lazy.txt}}
```
