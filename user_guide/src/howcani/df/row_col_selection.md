# 选中行或列

对行或列进行选择的操作与其他数据框架库类似。

## 选中列

```python
# 推荐写法
df.select(["a", "b"])
# 也可以写成这样
df(["a", "b"])
```

```text
{{#include ../../outputs/row_col_selection/col_selection.txt}}
```

## 选中行

```python
df[0:2]
```

```text
{{#include ../../outputs/row_col_selection/row_selection.txt}}
```
