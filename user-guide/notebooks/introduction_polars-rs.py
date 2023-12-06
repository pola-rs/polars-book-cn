#!/usr/bin/env python
# coding: utf-8

# > Note: To use this notebook, you must first install the [Rust `excvr` jupyter kernel](https://github.com/google/evcxr/blob/main/evcxr_jupyter/README.md).  Also, note that `clone()` is used fairly often in the examples.  This is because we tend to create one dataset for multiple examples.  When this dataset is used, the rust ownership system will `move` that dataframe, which will make it unavailable to later examples.  By `clone`ing, we can keep using it over and over.

# In[ ]:


:dep polars = {version = "0.23.2", features = ["lazy", "csv-file", "strings", "temporal", "dtype-duration", "dtype-categorical", "concat_str", "list", "list_eval", "rank", "lazy_regex"]}
:dep color-eyre = {version = "0.6.2"}
:dep rand = {version = "0.8.5"}
:dep reqwest = {version = "0.11.11", features = ["blocking"]}

use color_eyre::{Result};
use polars::prelude::*;


# # Expressions
# 
# `fn(Series) -> Series`
# 
# * Lazily evaluated
#     * Can be optimized
#     * Gives the library writer context and informed decisions can be made
# * Embarrassingly parallel
# * Context dependent
#     * selection/projection -> `Series` = *COLUMN, LITERAL, or VALUE*
#     * aggregation -> `Series` = *GROUPS*

# In[5]:


let df = df! [
    "A"        => [1, 2, 3, 4, 5],
    "fruits"   => ["banana", "banana", "apple", "apple", "banana"],
    "B"        => [5, 4, 3, 2, 1],
    "cars"     => ["beetle", "audi", "beetle", "beetle", "beetle"],
    "optional" => [Some(28), Some(300), None, Some(2), Some(-30)],
]?;
df


# # Selection context

# In[6]:


(/, We, can, select, by, name)
(/, We'll, be, re-using, the, dataframe, a, bunch,, so, we'll, clone, copies, as, we, go.)
df.clone().lazy().select([
    col("A"),
    col("B"),
    lit("B"),  // we must tell polars we mean the literal "B"
    col("fruits"),
]).collect()?


# In[7]:


(/, you, can, select, columns, with, a, regex, if, it, starts, with, '^', and, ends, with, '$')

df.clone().lazy().select([
    col("^A|B$").sum()
]).collect()?


# In[46]:


(/, you, can, select, multiple, columns, by, name)

df.clone().lazy().select([
    cols(["A", "B"]).sum()
]).collect()?


# In[8]:


(/, We, select, everything, in, normal, order)
(/, Then, we, select, everything, in, reversed, order)

df.clone().lazy().select([
    all(),
    all().reverse().suffix("_reverse")
]).collect()?


# In[9]:


(/, all, expressions, run, in, parallel)
(/, single, valued, `Series`, are, broadcasted, to, the, shape, of, the, `DataFrame`)

df.clone().lazy().select([
    all(),
    all().sum().suffix("_sum")
]).collect()?


# In[10]:


(/, there, are, `str`, and, `dt`, namespaces, for, specialized, functions)

let predicate = col("fruits").str().contains("^b.*");

df.clone().lazy().select([
    predicate
]).collect()?


# In[11]:


(/, use, the, predicate, to, filter)
let predicate = col("fruits").str().contains("^b.*");
df.clone().lazy().filter(predicate).collect()?


# In[12]:


(/, predicate, expressions, can, be, used, to, filter)

df.clone().lazy().select([
    col("A").filter(col("fruits").str().contains("^b.*")).sum(),
    (col("B").filter(col("cars").str().contains("^b.*")).sum() * col("B").sum()).alias("some_compute()"),
]).collect()?


# In[13]:


(/, We, can, do, arithmetic, on, columns, and, (literal), values)
(/, can, be, evaluated, to, 1, without, programmer, knowing)

let some_var = 1;

df.clone().lazy().select([
    ((col("A") / lit(124.0) * col("B")) / sum("B") * lit(some_var)).alias("computed")
]).collect()?


# In[17]:


(/, We, can, combine, columns, by, a, predicate)
(/, This, doesn't, work., It, seems, like, the, condition, always, evaluates, to, true)
df.clone().lazy().select([
    col("fruits"),
    col("B"),
    when(col("fruits") == lit("banana")).then(col("B")).otherwise(-1).alias("b when not banana")
]).collect()?


# In[15]:


(/, We, can, combine, columns, by, a, fold, operation, on, column, level)

df.clone().lazy().select([
    col("A"),
    col("B"),
    fold_exprs(lit(0), |a, b| Ok(&a + &b), [
        col("A"),
        lit("B"),
        col("B").pow(lit(2)),
        col("A") / lit(2.0)
    ]).alias("fold")
]).collect()?


# In[34]:


(/, even, combine, all)
use std::convert::TryInto;
let height: i32 = df.height().try_into()?;
df.clone().lazy().select([
    range(0i32, height).alias("idx"),
    col("A"),
    col("A").shift(1).alias("A_shifted"),
    concat_str([all()], "").alias("str_concat_1"),  // prefer this
    fold_exprs(col("A"), |a, b| Ok(a + b), [all().exclude(["A"])]).alias("str_concat_2"), // over this (accidentally O(n^2))
]).collect()?


# # Aggregation context
# 
# * expressions are applied over groups instead of columns
# 
# 

# In[35]:


(/, we, can, still, combine, many, expressions)

df.clone().lazy().sort("cars", SortOptions::default()).groupby(["fruits"])
    .agg([
        col("B").sum().alias("B_sum"),
        sum("B").alias("B_sum2"),  // syntactic sugar for the first
        col("fruits").first().alias("fruits_first"),
        col("A").count().alias("count"),
        col("cars").reverse()
    ]).collect()?


# In[37]:


(/, We, can, explode, the, list, column, "cars")

df.clone().lazy()
    .sort("cars", SortOptions { descending: false, nulls_last: false })
    .groupby(["fruits"])
    .agg([
        col("B").sum().alias("B_sum"),
        sum("B").alias("B_sum2"),  // syntactic sugar for the first
        col("fruits").first().alias("fruits_first"),
        col("A").count().alias("count"),
        col("cars").reverse()
    ])
    .explode(["cars"])
    .collect()?


# In[38]:


df.clone().lazy()
    .groupby(["fruits"])
    .agg([
        col("B").sum().alias("B_sum"),
        col("fruits").first().alias("fruits_first"),
        count(),
        col("B").shift(1).alias("B_shifted")
    ])
    .explode(["B_shifted"])
    .collect()?


# In[39]:


(/, we, can, also, get, the, list, of, the, groups)

df.clone().lazy()
    .groupby(["fruits"])
    .agg([
        col("B").shift(1).alias("shift_B"),
        col("B").reverse().alias("rev_B"),
    ])
    .collect()?


# In[40]:


(/, we, can, do, predicates, in, the, groupby, as, well)

df.clone().lazy()
    .groupby(["fruits"])
    .agg([
        col("B").filter(col("B").gt(lit(1))).list().keep_name(),
    ])
    .collect()?


# In[41]:


(/, and, sum, only, by, the, values, where, the, predicates, are, true)

df.clone().lazy()
    .groupby(["fruits"])
    .agg([
        col("B").filter(col("B").gt(lit(1))).mean(),
    ])
    .collect()?


# In[42]:


(/, Another, example)

df.clone().lazy()
    .groupby(["fruits"])
    .agg([
        col("B").shift_and_fill(1, 0).alias("shifted"),
        col("B").shift_and_fill(1, 0).sum().alias("shifted_sum"),
    ])
    .collect()?


# # Window functions!
# 
# * Expression with superpowers.
# * Aggregation in selection context
# 
# ```rust
# col("foo").aggregation_expression(..).over("column_used_to_group")
# ```

# In[43]:


(/, groupby, 2, different, columns)

df.clone().lazy()
    .select([
        col("fruits"),
        col("cars"),
        col("B"),
        col("B").sum().over(["fruits"]).alias("B_sum_by_fruits"),
        col("B").sum().over(["cars"]).alias("B_sum_by_cars"),
    ])
    .collect()?


# In[44]:


(/, reverse, B, by, groups, and, show, the, results, in, original, DF)

df.clone().lazy()
    .select([
        col("fruits"),
        col("B"),
        col("B").reverse().over(["fruits"]).alias("B_reversed_by_fruits")
    ])
    .collect()?


# In[45]:


(/, Lag, a, column, within, "fruits")

df.clone().lazy()
    .select([
        col("fruits"),
        col("B"),
        col("B").shift(1).over(["fruits"]).alias("lag_B_by_fruits")
    ])
    .collect()?


# In[ ]:




