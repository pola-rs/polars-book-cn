# 字符分隔值

## 读&写

读取CSV文件应该看起来很熟悉:

```python
df = pl.read_csv("path.csv")
```

CSV文件会有非常多的样式，所以一定要去看一下
[`read_csv()`](https://pola-rs.github.io/polars/py-polars/html/reference/api/polars.read_csv.html) API。

写入CSV文件可以用
[`write_csv()`](https://pola-rs.github.io/polars/py-polars/html/reference/api/polars.DataFrame.write_csv.html)方法。

```python
df = pl.DataFrame({"foo": [1, 2, 3], "bar": [None, "bak", "baz"]})
df.write_csv("path.csv")
```

## 扫描

`Polars`允许你*扫描*CSV文件。扫描操作延迟了对文件的实际解析，
并返回一个延迟计算的容器`LazyFrame`。

```python
df = pl.scan_csv("path.csv")
```

如果你想了解更多这样设计的精妙之处，
请移步`Polars`[Optimizations](../../optimizations/intro.md)这一章。
