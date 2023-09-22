from .dataset import df
import polars as pl

df = df.select(
    [
        pl.col("*"),  # 选择所有列
        pl.col("random").sum().over("groups").alias("sum[random]/groups"),
    ]
)
