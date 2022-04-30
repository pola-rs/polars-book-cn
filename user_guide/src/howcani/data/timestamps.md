# 时间戳解析

`Polars` 提供了`4`时间数据类型：

- `pl.Date`, 用于**日期**对象：自UNIX纪元以来的天数，为32位有符号整数。
- `pl.Datetime`, 用于**datetime**项目：自UNIX纪元以来的纳秒数，为64位有符号整数。
- `pl.Time`, 编码为午夜后的纳秒数。

`Polars` 字符串(`pl.Utf8`) 数据类型可以解析为它们中的任何一个。您可以让`Polars`尝试猜测日期\[time\]的格式，或者显式提供`fmt`规则。

举例来说（查看此[此链接](https://strftime.org/)以获取全面列表）：

- `"%Y-%m-%d"` 对于 `"2020-12-31"`
- `"%Y/%B/%d"` 对于 `"2020/December/31"`
- `"%B %y"` 对于 `"December 20"`

下面是一个简单的例子：

```python
{{#include ../../examples/timestamps/snippet.py}}
```

返回：

```text
{{#include ../../outputs/timestamps/output.txt}}
```

所有datetime功能都显示在 [`dt` 命名空间](POLARS_PY_REF_GUIDE/series.html#timeseries)中。
