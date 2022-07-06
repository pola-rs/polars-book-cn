from .dataset import df
import polars as pl

out = df.select(
    [
        pl.sum("nrs"),
        pl.col("names").sort(),  # 对names列进行排序
    ]
)
