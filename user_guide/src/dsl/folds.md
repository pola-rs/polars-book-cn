# Folds

`Polars` 提供了横向表达式或者方法，比如[`sum`](POLARS_PY_REF_GUIDE/api/polars.DataFrame.sum.html),
[`min`](POLARS_PY_REF_GUIDE/api/polars.DataFrame.min.html), [`mean`](POLARS_PY_REF_GUIDE/api/polars.DataFrame.mean.html) 等等，
我们只需要设置 `axis=1` 即可实现横向聚合。但是，当我们需要复杂的聚合模式时，`Polars` 提供的基本函数可能不能胜任，这时候我们需要 `fold` 函数。

`fold` 函数在列方向的性能最佳，它很好的利用了数据的内存格局，通常还会伴随向量化操作。

让我们通过里一个例子看看如何受使用 `fold` 实现 `sum` 函数。

## 手工 `sum`

```python
{{#include ../examples/expressions/fold_1.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/folds_1.txt}}
```

上面的例子中，函数 `f(acc, x) -> acc` 被反复调用并把结果累加到 `acc` 变量，最终把结果放入 x 列。
这个函数按照列执行，并且充分利用了缓存和向量化操作。

## 条件语句

当我们希望对一个 `DataFrame` 的所有列是施加条件语句的时候，采用 `fold` 就非常简洁。

```python
{{#include ../examples/expressions/fold_2.py:4:}}
print(out)
```

```text
{{#include ../outputs/expressions/folds_2.txt}}
```

上面的例子中，我们选择所有行，这些行的每一列都大于 1。

## `fold` 和 字符串数据

Fold 可以用来连接字符串。但是由于这个操作会产生一些中间结果，这个操作是 `O(n^2)` 的时间复杂度。
因此，我们推荐使用 `concat_str` 表达式。

```python
{{#include ../examples/expressions/fold_3.py:3:}}
print(out)
```

```text
{{#include ../outputs/expressions/folds_3.txt}}
```
