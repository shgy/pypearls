## htmlutil.py

有时, 我们可能有这样的需求: 根据数据生成HTML表格.

<img
  src="https://github.com/shgy/pypearls/blob/master/htmlutil.png"
  alt="pypearls"
  width="500"
/>

这看起来是一个很简单的任务, 实际上也确实是很简单的任务. 即使简单, 也有很好玩的地方:

1. 有合并单元格的表头, 怎么处理 ?
2. 数据的某一列, 需要高亮, 数值像股票一样显示红色或者绿色, 怎么做?

使用 htmlutil.py 可以应付这两个简单的问题.

htmlutil.py 是使用python (2.7) 编写的, 将数据以HTML table方式显示出来. 可用在 `数据可视化` 或 `发送指标监控邮件` 的一些场景中.



