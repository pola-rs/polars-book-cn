# polars-book-cn

[Read here the Chinese translation of the polars User Guide](https://pola-rs.github.io/polars-book-cn/user-guide/index.html)

这个仓库是 [Polars DataFrame library](https://github.com/pola-rs/polars) User Guide 的中文版本。

如果你对这个项目感兴趣，可以在 [user_guide/src](./user_guide/src/) 文件夹下找到需要翻译的内容，并将其翻译为中文版本。在参与贡献过程中请遵循[贡献指南](./CONTRIBUTING.md)来参与到该项目的协作中。

## 本地预览

在本地预览首先要安装 [`cargo`](https://doc.rust-lang.org/cargo/getting-started/installation.html)，在项目根目录执行以下命令即可创建本地预览
```bash
cargo install mdbook
cd user_guide
mdbook serve --hostname 0.0.0.0 --port 8000
```
打开浏览器输入 `localhost:8000` 即可查看在线文档。

## 参考指南

- [`Rust` 发行版本](https://docs.rs/polars/latest/polars/)
- [`Python` API](https://pola-rs.github.io/polars/py-polars/html/reference/)

## License

该项目采用的是[MIT 许可证](http://choosealicense.com/licenses/mit/)。