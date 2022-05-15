# 应用自定义函数

总会有一个操作非常特殊，以至于人们无法用`Polars`的公共API来完成它。幸运的是，polars允许您应用自定义函数。这意味着可以定义一个`Python`函数（或`lambda`），并将其传递给逻辑计划。

假设我们想要以一种迫切（eager）的方式将一个映射操作应用于一个`Polars` `Series`。这可以按如下所示进行：

```python
{{#include ../../examples/udfs/snippet1.py}}
```

返回：

```text
{{#include ../../outputs/udfs/output1.txt}}
```

然而，由于`Polars` `Series`只能包含一个数据类型，因此存在一些问题。

在上面的`apply()`方法中我们没有指定`Series`应该包含的数据类型`Polars`试图通过调用提供的函数本身来提前推断输出数据类型。如果它后来得到的数据类型与最初推断的类型不匹配，则该值将被指示为缺失（`null`）。

如果输出数据类型已知，建议将该信息提供给`Polars`（通过`.apply()`的`dtype`选项）。

注意，应用函数后可能会更改数据类型：我们上面使用的`lambda`得到一个整数作为输入，并在`my_map`字典中找到正确的键后返回一个字符串（`pl.Utf8`）。

# 使用map或者apply?

使用自定义函数有两种方法，一种是使用`map`，另一种是使用`apply`。您需要哪一个取决于使用自定义函数的上下文：

- `apply`

  - 选择上下文：自定义函数应用于所有值 `Fn(value) -> y`
  - 聚合上下文：自定义函数应用于所有组 `Fn([group_value_1, ... group_value_n]) -> y`

- `map`

  - 选择上下文：自定义函数应用于`Series`，并且必须生成一个新的`Series` `Fn(Series) -> Series`
  - 聚合上下文：自定义函数应用于`Series`，并且必须生成一个新的`Series` `Fn(Series) -> Series`
