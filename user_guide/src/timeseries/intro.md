# 时间序列

`Polars` 为时间序列重采样提供了强大的 API 支持。许多人都知道 `Pandas` 中 `df.resample` 提供了重采样功能。

`Polars` 在以下两个方面与 `Pandas` 有所区别：

- 上采样 (Upsampling)
- 下采样 (Downsampling)

## 上采样 (Upsampling)

上采样实际上相当于将一个日期范围与你的数据集进行左关联 (left join) 操作，并填充缺失数据。`Polars` 为此操作
提供了封装方法，你可以参考下面的一个示例。

## 下采样 (Downsampling)

下采样很有意思。你需要处理日期间隔、窗口持续时间、聚合等问题。

`Polars` 将下采样视为 **groupby** 操作的一个特例，因此表达式 API 为 **groupby** 上下文提供了两个额外的入口。

- [groupby_dynamic](POLARS_PY_REF_GUIDE/api/polars.DataFrame.groupby_dynamic.html)
- [groupby_rolling](POLARS_PY_REF_GUIDE/api/polars.DataFrame.groupby_rolling.html)

你可以通过调用二者其中任何一个函数来获取对表达式 API 的完整访问，它有着强大的性能！

让我们通过下面几个示例来理解这样做的意义。

## 动态分组 (Groupby Dynamic)

在下面的一段代码中，我们以 **天** (`"1d"`) 为单位，把关于 2021 年的 `日期范围 (date range)` 创建为一个 `DataFrame`。

接下来，我们创建起始于每 **月** (`"1mo"`)，长度为 `1` 个月的动态窗口 (dynamic windows)。动态窗口的大小并不由 `DataFrame`
中的行数决定，而是由一个时间单位 (temporal unit) 决定，比如一天 (`"1d"`)，三周 (`"3w"`)，亦或是五纳秒 (`"5ns"`) ...
希望这个例子有助于让你理解动态窗口的含义。

匹配某个动态窗口的值会被分配到该窗口所对应的组中，接下来你可以用强大的表达式 API 进行聚合操作。

下面的示例使用 **groupby_dynamic** 来计算：

- 距离月底的天数
- 一个月里的天数

```python
{{#include ../examples/time_series/days_month.py:4:}}
print(out)
```

```text
{{#include ../outputs/time_series/days_month.txt}}
```

要定义一个动态窗口，需要提供以下三个参数：

- **every**：窗口的时间间隔
- **period**：窗口的持续时间
- **offset**：可以对窗口的开始进行偏移

因为 _**every**_ 并不总是需要等于 _**period**_，我们可以用一种非常灵活的方式来创建很多组别。它们可以互相重叠，也可以在组间留出边界。

我们先从简单的例子开始 🥱 想想看下面几组参数会创建出怎么样的窗口。

>

- every: 1 天 -> `"1d"`
- period: 1 天 -> `"1d"`

```text
创建出的窗口相邻，且长度相等
|--|
   |--|
      |--|
```

>

- every: 1 天 -> `"1d"`
- period: 2 天 -> `"2d"`

```text
窗口之间有 1 天的重叠
|----|
   |----|
      |----|
```

>

- every: 2 天 -> `"2d"`
- period: 1 天 -> `"1d"`

```text
两个窗口之间留有间隔，在这段范围内的数据不属于任何一个组别
|--|
       |--|
              |--|
```

## 滚动分组 (Rolling Groupby)

滚动分组是 `groupby` 上下文的另一个入口。但与 `groupby_dynamic` 不同的是，窗口的设置不接受参数 `every` 和 `period` ——
对于一个滚动分组，窗口根本就不是固定的！它们由 `index_column` 中的值决定。

想象一下，你有一个值为`{2021-01-01, 20210-01-05}` 的时间序列，使用参数 `period="5d"` 将创建以下窗口：

```text

2021-01-01   2021-01-06
    |----------|

       2021-01-05   2021-01-10
             |----------|
```

由于滚动分组的窗口总是由 `DataFrame` 列中的值决定，组别的数目总是与原 `DataFrame` 相等。

## 将动态分组与滚动分组结合起来

用正常的 groupby 操作，我们可以将这两种分组方式结合起来。

下面是一个使用动态分组的例子：

```python
{{#include ../examples/time_series/dynamic_ds.py:0:}}
print(out)
```

```text
{{#include ../outputs/time_series/dyn_df.txt}}
```

```python
{{#include ../examples/time_series/dynamic_groupby.py:4:}}
print(out)
```

```text
{{#include ../outputs/time_series/dyn_gb.txt}}
```

## 上采样

> 该部分内容仍在编写。
