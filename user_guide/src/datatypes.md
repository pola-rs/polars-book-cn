# 数据类型

`Polars`完全基于`Arrow`数据类型，并由`Arrow`内存阵列支持。这使得数据处理
缓存效率高，支持进程间通信。大多数数据类型遵循确切的实现来自`Arrow`，除了`Utf8`（实际上是`LargeUtf8`）、`category`和`Object`（支持有限）。

这些数据类型是:

- `Int8`: 8位有符号整数。
- `Int16`: 16位有符号整数。
- `Int32`: 32位有符号整数。
- `Int64`: 64位有符号整数。
- `UInt8`: 8位有符号整数。
- `UInt16`: 16位无符号整数。
- `UInt32`: 32位无符号整数。
- `UInt64`: 64位无符号整数。
- `Float32`: 32位浮点数。
- `Float64`: 64位浮点数。
- `Boolean`: 布尔型有效位压缩。
- `Utf8`: 字符串数据（内部实际上是`Arrow ` `LargeUtf8`）。
- `List`: 列表数组包含着包含列表值的子数组和偏移数组。（这实际上是内部的`Arrow` `LargeList`）。
- `Date`: 日期表示，内部表示为自UNIX纪元以来的天数，由32位有符号整数编码。
- `Datetime`: Datetime表示法，内部表示为自UNIX纪元以来的纳秒，由64位有符号整数编码。
- `Duration`: 时间型。在减去`Date/Datetime`时创建。
- `Time`: 时间表示法，从午夜开始在内部表示为纳秒。
- `Object`: 受支持的有限数据类型，可以是任何值。

要了解有关这些数据类型的内部表示形式的更多信息，请查看[`Arrow`柱状格式](https://arrow.apache.org/docs/format/Columnar.html)。
