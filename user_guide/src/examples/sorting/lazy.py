from .dataset import df
import polars as pl

q = df.lazy().sort(pl.col("a"), descending=True)  # 惰性排序，对"a"列
df = q.collect()
