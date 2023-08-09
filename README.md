# polars-book-cn

[Read here the Chinese translation of the polars User Guide](https://pola-rs.github.io/polars-book-cn/user-guide/index.html)

这个仓库是 [Polars DataFrame library](https://github.com/pola-rs/polars) User Guide 的中文版本。

This repository is the Chinese version of the [Polars DataFrame library](https://github.com/pola-rs/polars) User Guide.

## 本地预览

在本地预览首先要安装 [`cargo`](https://doc.rust-lang.org/cargo/getting-started/installation.html)，在项目根目录执行以下命令即可创建本地预览

```bash
cargo install mdbook
cd user_guide
mdbook serve --hostname 0.0.0.0 --port 8000
```
打开浏览器输入 `localhost:8000` 即可查看在线文档。

## 贡献指南

在 [user_guide/src](./user_guide/src/) 文件夹下找到需要补充的内容:

- [中文文档：pola-rs/polars-book-cn](https://pola-rs.github.io/polars-book-cn/user-guide/index.html)
- [英文文档：pola-rs/polars-book](https://pola-rs.github.io/polars-book/user-guide/index.html)

请遵循[贡献指南](./CONTRIBUTING.md)来参与到项目的协作与完善中，[尝试案例](https://github.com/pola-rs/polars-book-cn/tree/main/user_guide/src/examples)并结合最新的英文文档来获取更多内容。

## 参考学习

- [`Python` API](https://pola-rs.github.io/polars/py-polars/html/reference/)
- [`Rust` 发行版本](https://docs.rs/polars/latest/polars/)

## License

[MIT 许可证](http://choosealicense.com/licenses/mit/)