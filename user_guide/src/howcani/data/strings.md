# 处理字符串

感谢`Arrow` 后端, `Polars`字符串操作比使用`NumPy`或`Pandas`执行的相同操作快得多。在后者中，字符串存储为`Python`对象。 在遍历`np.array` or the `pd.Series`时，CPU需要跟踪所有字符串指针，并跳转到许多随机内存位置——这是非常低效的缓存。在`Polars`（通过`Arrow`数据结构）中，字符串在内存中是连续的。因此，对于CPU来说，遍历缓存是最优的，也是可预测的。

`Polars`中可用的字符串处理函数可以在 [\`\`str\` namespace](POLARS_PY_REF_GUIDE/series.html#strings) 中找到。

下面是几个例子。要计算字符串长度，请执行以下操作：

```python
{{#include ../../examples/strings/snippet1.py}}
```

返回：

```text
{{#include ../../outputs/strings/output1.txt}}
```

下面是从句子中过滤出冠词（`the`、`a`、`and`、*etc.*）的正则表达式模式：

```python
{{#include ../../examples/strings/snippet2.py}}
```

输出：

```text
{{#include ../../outputs/strings/output2.txt}}
```
