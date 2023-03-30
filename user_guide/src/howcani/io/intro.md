# IO

`Polars`支持不同的文件类型，其各自的解析器都是最快的。

例如，在将CSV文件交给`Pandas`之前，通过`Polars`加载CSV文件比使用`Pandas`加载要快。只需运行 `pl.read_csv（"<FILE>"，rechunk=False）.to_pandas()`。
