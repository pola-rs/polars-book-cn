# 串

了解`Arrow`和`Polars`使用的内存格式可以真正提高查询的性能. 对于大型字符串数据尤其如此。下图显示了`Arrow` `UTF8`数组在内存中的布局。

数组`[“foo”、“bar”、“ham”]`由以下编码：

- 连接字符串`foobarham`，
- 一个偏移数组，指示每个字符串`[0,2,5,8]`的开始（和结束），
- 空位图，指示空值。

![](https://raw.githubusercontent.com/pola-rs/polars-static/master/docs/arrow-string.svg)

如果我们要读取字符串值，这种内存结构的缓存效率非常高。
尤其是如果我们将它与`Vec<String>`（在`Rust`中由堆分配的字符串数据组成的数组）进行比较。

![](https://raw.githubusercontent.com/pola-rs/polars-static/master/docs/pandas-string.svg)

然而，如果我们需要对`Arrow` `UTF8`数组重新排序，我们需要交换字符串值的所有字节，这在处理大型字符串时可能会非常昂贵。另一方面，对于`Vec<String>`，我们只需要交换指针，只需移动8字节的数据，成本很低。
由于一项操作（过滤、连接、分组*等*）而嵌入大量`Utf8` `Series`的`DataFrame`的重新排序可能很快变得非常昂贵。

## 范畴型

因此，`Polars`有一个`CategoricalType`。`category` `Series`是一个数组，其中填充了`u32`值，每个值代表一个唯一的字符串值。因此，在保持缓存效率的同时，移动值的成本也很低。

在下面的示例中，我们将演示如何将一个`Utf8` `Series`列强制转换为一个`Categorical` `Series`。

```python
import polars as pl

df["utf8-column"].cast(pl.Categorical)
```

### 在分类数据上加入多个数据帧

当需要基于字符串数据连接两个`DataFrame`时，需要同步`Category`数据（`df1`的`A`列中的数据需要指向与`df2`中的`B`列相同的底层字符串数据）。可以通过在`StringCache`上下文管理器中强制转换数据来实现。这将在该上下文管理器期间同步所有可发现的字符串值。如果希望全局字符串缓存在整个运行期间存在，可以将`toggle_string_cache`设置为`True`。

```python
{{#include ../examples/strings_performance/snippet1.py}}
```

### 惰性连接分类数据上的多个数据帧

在查询期间（直到调用`.collect()`），惰性查询始终具有全局字符串缓存（除非您选择退出）。下面的示例显示了如何将两个`DataFrame`与`Category`类型连接起来。

```python
{{#include ../examples/strings_performance/snippet2.py}}
```
