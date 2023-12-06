import polars as pl
from datetime import datetime

lazy_select_df = pl.scan_csv("data/appleStock.csv").select(["Date"])

lazy_select_df = lazy_select_df.explain()
