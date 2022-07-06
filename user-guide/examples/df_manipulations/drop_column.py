from .dataset import df
import polars as pl

# 删除单独的列
out = df.drop("d")

# 删除多个列
out = df.drop(["b", "c"])

# 选择所有列但是不包括('b', 'c')
out = df.select(pl.all().exclude(["b", "c"]))

# 仅选择列"a"
out = df.select(pl.col("a"))
