# 聚合

你可以调用 `.select()` 函数或使用 `.with_column()`/`.with_columns()` 上下文进行列聚合操作。

要对所有列进行聚合，可以使用通配符表达式：
`.select(pl.col("*").sum())`。

以下面的代码为例：

```python
{{#include ../../examples/aggregate/snippet.py}}
```

其结果为：

```text
{{#include ../../outputs/aggregate/output.txt}}
```

更多内容请参见[表达式](POLARS_PY_REF_GUIDE/expression.html#aggregation) 的 API 文档。
