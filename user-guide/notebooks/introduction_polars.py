#!/usr/bin/env python
# coding: utf-8

# In[1]:


import polars as pl


# # 表达式
# 
# `fn(Series) -> Series`
# 
# * 懒惰评估
#     - 可以被优化
#     - 向库提供背景信息，并做出明智的决定
# * 高度并行
# * 上下文相关
#     - 选择 / 投影 -> `Series` = **列、文本或值**
#     - 聚合 -> `Series` = **组**
# 

# In[2]:


df = pl.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "fruits": ["banana", "banana", "apple", "apple", "banana"],
        "B": [5, 4, 3, 2, 1],
        "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
        "optional": [28, 300, None, 2, -30],
    }
)
df


# # 选择上下文

# In[3]:


# 我们可以通过名称来选择

(df.select([
    pl.col("A"),
    "B",      # "B"这一列将会被推理
    pl.lit("B"),  # 我们必须告诉Polars, 我们"B"的文字信息
    pl.col("fruits"),
]))


# In[4]:


# 可以通过正则表达式（起始为‘^’终止为'$'）来选择列

(df.select([
    pl.col("^A|B$").sum() # 求和
]))


# In[5]:


# 可以通过名称选取多个列

(df.select([
    pl.col(["A", "B"]).sum() # 求和
]))


# In[6]:


# 我们可以以正常顺序选择所有事物
# 然后我们可以以逆序的方式选择事物

(df.select([
    pl.all(),
    pl.all().reverse().suffix("_reverse") # 表格中所有列逆序（并且文字中后缀为_reverse
]))


# In[7]:


# 所有表达式并行地运行
# 单值'Series'被广播到'DataFrame'的形状`

(df.select([
    pl.all(),
    pl.all().sum().suffix("_sum")
]))


# In[8]:


# 专门函数有'str'和'dt'名称空间

predicate = pl.col("fruits").str.contains("^b.*")

(df.select([
    predicate
]))


# In[9]:


# 利用谓语（predicate）进行过滤

df.filter(predicate)


# In[10]:


# 谓语（predicate） 表达式可以被用于过滤

(df.select([
    pl.col("A").filter(pl.col("fruits").str.contains("^b.*")).sum(),
    (pl.col("B").filter(pl.col("cars").str.contains("^b.*")).sum() * pl.col("B").sum()).alias("some_compute()"), # .alias方法表示另起一列
]))


# In[11]:


# 我们可以对列和（文字）值进行算术运算
# 可以在程序员不知道的情况下计算为1

some_var = 1

(df.select([
    ((pl.col("A") / 124.0 * pl.col("B")) / pl.sum("B") * some_var).alias("computed")
]))


# In[12]:


# 我们可以通过谓词（predicate）来组合列

(df.select([
    "fruits",
    "B",
    pl.when(pl.col("fruits") == "banana").then(pl.col("B")).otherwise(-1).alias("b")
]))


# In[13]:


# 我们可以在列这一层通过折叠操作组合列

(df.select([
    "A",
    "B",
    pl.fold(0, lambda a, b: a + b, [pl.col("A"), "B", pl.col("B")**2, pl.col("A") / 2.0]).alias("fold")
]))


# In[14]:


# 甚至组合所有

(df.select([
    pl.arange(0, df.height).alias("idx"),
    "A",
    pl.col("A").shift().alias("A_shifted"),
    pl.concat_str(pl.all(), "-").alias("str_concat_1"),  # 倾向于这种方式
    pl.fold(pl.col("A"), lambda a, b: a + "-" + b, pl.all().exclude("A")).alias("str_concat_2"),
]))


# # 聚合上下文
# * 表达式应用于组而不是列

# In[15]:


# 我们仍可以组合很多表达式

(df.sort("cars").groupby("fruits")
    .agg([
        pl.col("B").sum().alias("B_sum"),
        pl.sum("B").alias("B_sum2"),  # 第一个是语法糖
        pl.first("fruits").alias("fruits_first"),
        pl.count("A").alias("count"),
        pl.col("cars").reverse()
    ]))


# In[16]:


# 我们可以从“汽车”列下手

(df.sort("cars").groupby("fruits")
    .agg([
        pl.col("B").sum().alias("B_sum"),
        pl.sum("B").alias("B_sum2"),  # 第一个是语法糖
        pl.first("fruits").alias("fruits_first"),
        pl.count("A").alias("count"),
        pl.col("cars").reverse()
    ])).explode("cars")


# In[17]:


(df.groupby("fruits")
    .agg([
        pl.col("B").sum().alias("B_sum"),
        pl.sum("B").alias("B_sum2"),  # 第一个是语法糖
        pl.first("fruits").alias("fruits_first"),
        pl.count(),
        pl.col("B").shift().alias("B_shifted")
    ])
 .explode("B_shifted")
)


# In[18]:


# 我们可以从“汽车”列下手

(df.sort("cars").groupby("fruits")
    .agg([
        pl.col("B").sum(),
        pl.sum("B").alias("B_sum2"),  # 第一个是语法糖
        pl.first("fruits").alias("fruits_first"),
        pl.count("A").alias("count"),
        pl.col("cars").reverse()
    ])).explode("cars")


# In[19]:


# 我们也可以得到一列组

(df.groupby("fruits")
    .agg([
         pl.col("B").shift().alias("shift_B"),
         pl.col("B").reverse().alias("rev_B"),
    ]))


# In[20]:


# 我们也可以在groupby中使用谓词

(df.groupby("fruits")
    .agg([
        pl.col("B").filter(pl.col("B") > 1).list().keep_name(),
    ]))


# In[21]:


# 并且只根据谓词为真的值求和

(df.groupby("fruits")
    .agg([
        pl.col("B").filter(pl.col("B") > 1).mean(),
    ]))


# In[22]:


# 另一个例子

(df.groupby("fruits")
    .agg([
        pl.col("B").shift_and_fill(1, fill_value=0).alias("shifted"),
        pl.col("B").shift_and_fill(1, fill_value=0).sum().alias("shifted_sum"),
    ]))


# # 窗口函数!
# 
# * 用“超能力表”达。
# * 选择上下文中的聚合
# 
# 
# ```python
# pl.col("foo").aggregation_expression(..).over("column_used_to_group")
# ```
# 

# In[23]:


# groupby 2个不同的列

(df.select([
    "fruits",
    "cars",
    "B",
    pl.col("B").sum().over("fruits").alias("B_sum_by_fruits"),
    pl.col("B").sum().over("cars").alias("B_sum_by_cars"),
]))


# In[24]:


# 按组反转B，并在原始df中显示结果

(df.select([
    "fruits",
    "B",
    pl.col("B").reverse().over("fruits").alias("B_reversed_by_fruits")
]))


# In[25]:


# 将一列置于“fruits”中

(df.select([
    "fruits",
    "B",
    pl.col("B").shift().over("fruits").alias("lag_B_by_fruits")
]))

