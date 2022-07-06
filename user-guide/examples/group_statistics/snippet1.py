import polars as pl

from .dataset import parsed_sorted as dataset


# 创造一个新的Polars。每行序列有差异
def mkdiff(cumcases: pl.Series) -> pl.Series:
    return cumcases - cumcases.shift(1)


# 按uid分组并聚合到不同的系列列表中，我们稍后将其分解并合并
# 回到主数据帧
# mkdiff函数获取每个组的日期排序值
q = (
    dataset.groupby("country")
    .agg(
        [
            pl.col("date").list().alias("date"),
            pl.col("cumcases").apply(mkdiff).alias("diff"),
        ]
    )
    .explode(["date", "diff"])
    .join(dataset, on=["country", "date"])
)

df = q.collect()
