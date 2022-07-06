import numpy as np
import polars as pl

country = [x for i in [4 * [c] for c in ["belgium", "united-kingdom", "china"]] for x in i]
date = ["2020-12-20", "2020-12-21", "2020-12-22", "2020-12-23"]
cumcases = [23, 42, 67, 85]

# 构造DataFrame（数据帧）
raw_data = pl.DataFrame(
    {
        "country": country,
        "date": np.hstack([date, date, date]),
        "cumcases": np.hstack([cumcases, [2 * c for c in cumcases], [3 * c for c in cumcases]]),
    }
)

# 将第一列解析为date
# 接下来创建一个由组uid+date_integer整数定义的排序键
# 对排序键上的所有值进行排序，以便
parsed_sorted = (
    raw_data.lazy()
    .with_column(pl.col("date").str.parse_date(pl.Date))
    .with_column((pl.col("country").cast(str) + pl.lit("-") + pl.col("date").cast(int)).alias("sort_key"))
    .sort("sort_key")
)

df = parsed_sorted.collect()
