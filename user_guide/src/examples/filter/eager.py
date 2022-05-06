import polars as pl

df = pl.DataFrame({"a": [1, 2, 3], "b": [None, "b", "c"]})

mask = df["a"] > 2  # 谓词表达式
out = df[mask]  # 谓词过滤
