# polars-book-cn

[Read here the Chinese translation of the polars User Guide](https://pola-rs.github.io/polars-book-cn/user-guide/index.html)

这个仓库是 [Polars DataFrame library](https://github.com/pola-rs/polars) User Guide 的中文版本。

## Contribution

我们希望找到更多对 `Polars` 感兴趣的人参与到翻译工作中。如果你对这个项目感兴趣，可以执行以下三个步骤：

- 浏览 [Issue 列表](https://github.com/pola-rs/polars-book-cn/issues)找到没有被 assign 的 issue，然后评论 I will take it，我们会将这个 issue assign 分配给你
- 然后你可以在 [user_guide/src](./user_guide/src/) 文件夹下找到你想要翻译的内容，并将其翻译为中文版本即可，在参与贡献过程中需要遵循[贡献指南](./CONTRIBUTING.md)来参与到该项目的协作中
- 加入到我们的 [Discord](https://discord.com/invite/4UfP5cfBE7) 进行更加及时的讨论

## 本地预览
在本地预览首先要安装 [`cargo`](https://doc.rust-lang.org/cargo/getting-started/installation.html)，在项目根目录执行以下命令即可创建本地预览
```bash
cargo install mdbook
cd user_guide
mdbook serve --hostname 0.0.0.0 --port 8000
```
打开浏览器输入 `localhost:8000` 即可查看在线文档。

## License

该项目采用的是[MIT许可证](http://choosealicense.com/licenses/mit/)。 如果您有这方面的顾虑，请随时联系维护者。