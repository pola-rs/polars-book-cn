# Numpy

`Polars` 的 `Series` 支持 `NumPy` 的
[通用函数 (ufuncs)](https://numpy.org/doc/stable/reference/ufuncs.html)。
调用元素层面的 (element-wise) 函数，比如 `np.exp()`、`np.cos()` 或 `np.div()`，基本上没有额外开销。

需要注意的是，`Polars` 中的缺失值是一个独立的比特掩码 —— 其在 `NumPy` 中是不可见的。
这可能导致窗口函数或 `np.convolve()` 输出有缺陷或不完整的结果。

要将一个 `Polars` `Series` 转换为 `NumPy` 数组，可以调用 `.to_numpy()` 函数。
转换时，此函数将会把缺失值替换为 `np.nan`。如果 `Series` 中没有缺失值，或转换后不再需要这些值，
可以使用 `.view()` 函数作为代替，这将为数据生成一个零拷贝的 `NumPy` 数组。
