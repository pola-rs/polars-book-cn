from .dataset import df
import polars as pl

out = df.select(
    [
        pl.col("names").filter(pl.col("names").str.contains(r"am$")).count(),  # str命名空间使用正则表达式
    ]
)
