from .dataset import df

df = df.clone()
mask = df["range"] >= 5  # 谓词选取
df[mask, "range"] = 12  # 根据标量选取
