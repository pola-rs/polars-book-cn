## 处理多个文件

`Polars`可以根据您的需要和内存紧张程度，以不同的方式处理多个文件。

让我们创建一些文件来使用一些上下文（context）：

```python
{{#include ../examples/multiple_files/dataset.py:0:}}
```

## 读入单个`DataFrame`

要将多个文件读入一个`DataFrame`，我们可以使用全局模式：

```python
{{#include ../examples/multiple_files/single_df.py:3:}}
print(df)
```

```text
{{#include ../outputs/multiple_files/single_df.txt}}
```

要了解这是如何工作的，我们可以看看查询计划。下面我们可以看到，所有文件都是单独读取并连接成一个`DataFrame` 。`Polars`将尝试将读取并行化。

```python
pl.scan_csv("my_many_files_*.csv").show_graph()
```

![single_df_graph](../outputs/multiple_files/single_df_graph.png)

## 并行读取和处理

如果您的文件不必位于单个表中，您还可以为每个文件构建一个查询计划，并在`Polars`线程池中并行执行它们。所有查询计划的执行都是极好的并行执行，不需要任何通信。

```python
{{#include ../examples/multiple_files/multiple_queries.py:1:}}
print(dataframes)
```

```text
{{#include ../outputs/multiple_files/dataframes.txt}}
```
