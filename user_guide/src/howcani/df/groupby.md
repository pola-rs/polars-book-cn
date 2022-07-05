# 分组

## 急性 & 惰性

分组操作的语法在两个 API 中是类似的 —— 二者中均可使用表达式。
要完成分组操作，先调用 `.groupby()` 函数，并跟随一个 `.agg()` 函数。

在 `.agg()` 函数中，你可以对任意数量的列进行任意聚合操作。
要对所有列进行聚合，可以使用通配符表达式：
`.agg(pl.col("*").sum())`。

来看一个简单的（惰性）例子：

```python
{{#include ../../examples/groupby/snippet.py}}
```

这将返回下面的结果：

```text
{{#include ../../outputs/groupby/output.txt}}
```
