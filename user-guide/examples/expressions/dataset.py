import polars as pl
import numpy as np

np.random.seed(12)  # 设置随机数种子（保证每次生成的随机数相同）

df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", None],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
