from .dataset import df
import polars as pl

out = df.select(
    [
        pl.sum("random").alias("sum"),  # 对random列求和并新增一列
        pl.min("random").alias("min"),  # 对random列求最小值并新增一列
        pl.max("random").alias("max"),  # 对random列求最大值并新增一列
        pl.col("random").max().alias("other_max"),  # 另一种求最大值的方式
        pl.std("random").alias("std dev"),  # 对random列求标准差并新增一列
        pl.var("random").alias("variance"),  # 对random列求方差并新增一列
    ]
)
