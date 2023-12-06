import polars as pl
from datetime import datetime

# 时间轴（从low到high，间隔为1天，轴名称为"time"）
df = pl.date_range(start=datetime(2021, 1, 1), 
                   end=datetime(2021, 12, 31), 
                   interval="1d", 
                   name="time", 
                   eager=True).to_frame()

out = (
    df.groupby_dynamic("time", every="1mo", period="1mo", closed="left")
    .agg(
        [
            pl.col("time").cumcount().reverse().head(3).alias("day/eom"),
            ((pl.col("time") - pl.col("time").first()).last().dt.days() + 1).alias("days_in_month"),
        ]
    )
    .explode("day/eom")
)
