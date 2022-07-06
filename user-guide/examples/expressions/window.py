from .dataset import df
import polars as pl

df = df[
    [
        pl.col("*"),  # 选择所有列
        pl.col("random").sum().over("groups").alias("sum[random]/groups"),
        pl.col("random").list().over("names").alias("random/name"),
    ]
]
