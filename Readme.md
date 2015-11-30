# Project 1 建立一个搜索引擎
				
			
##### 朱文豪（5130309717） 刘多闻（5130309723）

------

## 使用说明


总共包含3部分

- 网页爬虫
- 生成索引
- 搜索页面

> 网页爬虫利用python实现。首先将网页url打开，之后利用正则表达式匹配相关信息并爬取。利用beautifulSoup包对爬去网页内容进行处理，只保留有用的文本信息，删除网页结构信息等。

> 生成索引功能基于Hadoop mapreduce以及中文分词工具IKAnalyzer实现。将爬取文档上传至hdfs，运行包含分词功能的mapreduce程序即可得到索引。

 > 搜索页面基于 `flask` 和 `bootstrap` 实现， 使用 `jinja2` 模板动态生成页面。
使用响应式布局，特别基于移动端进行优化。


####  1. 在线Demo

[http://exciting.delvin.xyz](http://exciting.delvin.xyz)

#### 2. 本地运行

```
$ pip install -r requirements.txt
$ cd /website/app
$ python app.py
```

访问 localhost(0.0.0.0):5000 即可演示










