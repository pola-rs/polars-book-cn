import polars as pl

from .dataset import parsed_sorted as dataset


# 创造一个新的polars。每行序列有差异
def mkdiff(cumcases: pl.Series) -> pl.Series:
    return cumcases - cumcases.shift(1)


q = dataset.with_column(
    pl.col("cumcases").apply(mkdiff).over("country").take(pl.col("country").arg_unique()).explode().alias("diffcases"),
)

df = q.collect()
