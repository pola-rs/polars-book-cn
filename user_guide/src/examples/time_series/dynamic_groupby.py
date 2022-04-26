from .dynamic_ds import df
import polars as pl

# 动态分组
out = df.groupby_dynamic(
    "time",
    every="1h",
    closed="both",
    by="groups",
    include_boundaries=True,
).agg([pl.count()])
