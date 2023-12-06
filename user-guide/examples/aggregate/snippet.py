import polars as pl

# 扫描级导入csv数据集
q = pl.scan_csv("data/reddit.csv").select([pl.sum("comment_karma"), pl.min("link_karma")])

df = q.fetch()
