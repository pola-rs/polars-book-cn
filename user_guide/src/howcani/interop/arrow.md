# Arrow

`Arrow` 正在迅速地成为列式数据 _事实上_ 的标准。这意味着对 `Arrow` 的支持（包括语言与工具）也在迅速增加。
由于开发者在这种格式的背后投入了大量的努力与支持，使用 `Arrow` 可能是完成下面任务最快的方式：

- 读写 `Parquet` 格式的文件
- 从 CSV 读取列式数据
- 交换列式数据

`Polars` 使用 `Arrow` 内存缓冲作为 `Polars` `Series` 最基本的构建模块。
这意味着当我们要在 `Polars` 和 `Arrow` 之间交换数据时，无需对数据进行**拷贝**操作。
这也意味着 `Polars` 获得了 `Arrow` 带来的一切性能提升。

要将 `Polars` 的 `DataFrame` 或者 `Series` 转换为 `Arrow`，只需使用 `.to_arrow()` 函数。
类似的，要从 `Arrow` 格式导入数据，可以调用 `.from_arrow()` 函数。
