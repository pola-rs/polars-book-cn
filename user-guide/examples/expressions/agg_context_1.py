from .dataset import df
import polars as pl

out = df.groupby("groups").agg(
    [
        pl.sum("nrs"),  # 通过groups列对nrs求和
        pl.col("random").count().alias("count"),  # 记录组数
        # 如果name != null记录random列的和
        pl.col("random").filter(pl.col("names").is_not_null()).sum().suffix("_sum"),
        pl.col("names").reverse().alias(("reversed names")),
    ]
)
