from .dataset import df
import polars as pl

df = df.with_columns(
    [
        pl.sum("nrs").alias("nrs_sum"),
        pl.col("random").count().alias("count"),
    ]
)
from .dataset import df
import polars as pl

df = df.with_columns(
    [
        pl.sum("nrs").alias("nrs_sum"),
        pl.col("random").count().alias("count"),
    ]
)
from .dataset import df
import polars as pl

df = df.with_columns(
    [
        pl.sum("nrs").alias("nrs_sum"),
        pl.col("random").count().alias("count"),
    ]
)
