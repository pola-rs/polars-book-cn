# Parquet

加载或写入 [`Parquet`文件](https://parquet.apache.org/)快如闪电。

`Pandas` 使用 [`PyArrow`](https://arrow.apache.org/docs/python/)（用于Apache `Arrow`的`Python`库）将`Parquet`数据加载到内存，但不得不将数据复制到了`Pandas`的内存空间中。

`Polars`就没有这部分额外的内存开销，因为读取`Parquet`时，`Polars`会直接复制进`Arrow`的内存空间，且*始终使用这块内存*。

## 读&写

```python
df = pl.read_parquet("path.parquet")
```

```python
df = pl.DataFrame({"foo": [1, 2, 3], "bar": [None, "bak", "baz"]})
df.write_parquet("path.parquet")
```

## 扫描

Polars允许你扫描`Parquet`输入。扫描操作延迟了对文件的实际解析，并返回一个延迟计算的容器`LazyFrame`。

```python
df = pl.scan_parquet("path.parquet")
```

如果你想了解更多这样设计的精妙之处，请移步`Polars`[Optimizations](../../optimizations/intro.md)这一章。
