# 与Numpy交互

`Polars` 表达式支持`NumPy` [ufuncs](https://numpy.org/doc/stable/reference/ufuncs.html)。 [这里](https://numpy.org/doc/stable/reference/ufuncs.html#available-ufuncs)查看所有受支持的numpy函数的列表。

这意味着，如果一个函数不是由`Polars`提供的，我们可以使用`NumPy`，我们仍然可以通过`NumPy`API进行快速的列操作。

## 实例

```python
{{#include ../examples/expressions/numpy_ufunc.py}}
print(out)
```

```text
{{#include ../outputs/expressions/np_ufunc_1.txt}}
```

## Gotcha's

阅读更多关于 [gotcha's 这里](POLARS_ROOT/howcani/interop/numpy.html).
