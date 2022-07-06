import numpy as np
import polars as pl

# 构造数据帧
df = pl.DataFrame({"range": np.arange(10), "left": ["foo"] * 10, "right": ["bar"] * 10})
