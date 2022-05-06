from .dataset import df

out = df.sort(["b", "a"], reverse=[True, False])  # 分别对两列"b", "a"进行排序，"b"逆序，"a"顺序
