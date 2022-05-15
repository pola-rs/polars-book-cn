# 应用窗口函数

`Polars` 支持窗口函数，灵感来自于[PostgreSQL](https://www.postgresql.org/docs/current/tutorial-window.html). `Pandas` 用户可能会将其识别为a `groupby.transform(aggregation)`.

`Polars` 窗口函数比`Pandas`转换（transform）函数更加优雅. 我们可以在一个表达式中的多个列上应用多个函数！

```python
{{#include ../../examples/window_functions/snippet.py}}
```

```text
{{#include ../../outputs/window_functions/output.txt}}
```
