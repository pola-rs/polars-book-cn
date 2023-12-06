import numpy as np
import polars as pl

np.random.seed(42)  # 设置随机数种子（保证每次运行产生的随机数相同）

df = pl.DataFrame(
    {
        "a": [1, 2, 3, None, 5],
        "b": ["foo", "ham", "spam", "egg", None],
        "c": np.random.rand(5),
        "d": ["a", "b", "c", "d", "e"],
    }
)
