# 与AWS互动

> "与AWS互动"页面正在建设中。

要读取或写入AWS存储桶，需要额外的依赖项：

```shell
$ pip install s3fs
```

在接下来的几个片段中，我们将演示如何与`Parquet`文件交互位于AWS桶上。

## 读入

使用如下加载一个`.parquet`：

```python
import polars as pl
import pyarrow.parquet as pq
import s3fs

fs = s3fs.S3FileSystem()
bucket = "<YOUR_BUCKET>"
path = "<YOUR_PATH>"

dataset = pq.ParquetDataset(f"s3://{bucket}/{path}", filesystem=fs)
df = pl.from_arrow(dataset.read())
```

## 写入

> 该内容正在建设中。
