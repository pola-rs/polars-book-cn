# 与Postgres交互

## 读取

从postgres数据库中读取数据，需要额外依赖项:

```shell
$  pip install connectorx>=0.2.0a3
```

```python
import polars as pl

conn = "postgresql://username:password@server:port/database"
query = "SELECT * FROM foo"

pl.read_sql(query, conn)
```

## 写入

写入postgres数据库，需要额外依赖项:

```shell
$ pip install psycopg2-binary
```

用`psycopg2`写入postgres数据库，我们会用`批处理`的方法，限制与服务器的往返行程以提高写入性能。

我们首先要保证所有的数据类型可以被`psycopg2`所识别，再使用`DataFrame.rows`轻松将每列数据转置成数据库驱动程序可以处理的行。

```python
from psycopg2 import sql
import psycopg2.extras
import polars as pl

# 不仿假设有一个DataFrame，其列分别为：浮点，整数，字符串，日期（date64）类型的数据
df = pl.read_parquet("somefile.parquet")

# 首先将 polars 的 date64 数据类型转换成 python 的 datetime 对象
for col in df:
    # 只转换date64类型数据
    if col.dtype == pl.Date64:
        df = df.with_column(col.dt.to_python_datetime())

# 为字段名创建 sql 标识符
# 这一步是为了在sql语句中安全插入数据
columns = sql.SQL(",").join(sql.Identifier(name) for name in df.columns)

# 为值创建占位符，之后再被值填充
values = sql.SQL(",").join([sql.Placeholder() for _ in df.columns])

table_id = "mytable"

# 准备insert语句
insert_stmt = sql.SQL("INSERT INTO ({}) VALUES({});").format(
    sql.Identifier(table_id), columns, values
)

# 创建与数据库的连接
conn = psycopg2.connect()
cur = conn.cursort()

# 执行insert语句
psycopg2.extras.execute_batch(cur, insert_stmt, df.rows())
conn.commit()
```
