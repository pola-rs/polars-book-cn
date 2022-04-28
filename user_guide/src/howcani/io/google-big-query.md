# 与Google的BigQuery交互

读写BigQuery数据库，需要额外依赖项：

```shell
$ pip install google-cloud-bigquery
```

## 读取

从BigQuery查询并得到`DataFrame`，可以像这样：

```python
import polars as pl
from google.cloud import bigquery

client = bigquery.Client()

# 执行查询
QUERY = (
    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
    'WHERE state = "TX" '
    'LIMIT 100')
query_job = client.query(QUERY)  # API 请求
rows = query_job.result()  # 等待查询完成

df = pl.from_arrow(rows.to_arrow())
```

## 写入

> 内容还在建设中
