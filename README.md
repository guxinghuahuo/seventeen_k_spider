# Seventeen_K_Spider

刚开始学爬虫，这是一个练手用的项目，命名不规范见谅。用 Scrapy 编写的爬虫项目，旨在从 [Starbucks](https://www.17k.com/all/book/2_0_0_0_3_0_1_0_1.html) 网站爬取小说信息。参照知乎专栏`https://zhuanlan.zhihu.com/p/551275060`写的，不过网站已经添加了反爬技术，所有网页采用动态渲染，导致专栏中的代码无法正常运行。本项目在此基础上增加了 splash 模拟访问。

## 功能描述

- **提取小说信息**：从免费小说页面逐级提取小说信息，包括小说名称、作者、分类、封面图片 URL、简介、最新章节、最新章节 URL、评分、字数、更新时间等。

## 目录结构

```
Seventeen_K_Spider/
├── spider/               # Scrapy 爬虫脚本目录
├── utils/                # 工具类目录
└── README.md             # 项目文档
```

## 项目依赖

- **运行环境**: Python 3.9.21。

### 安装依赖

   ```bash
   pip install scrapy==2.11.0
   pip install scrapy-splash
   ```

## 如何运行

1. **配置 Splash 服务器**：

   下载并启动 Splash 服务器。

   ```bash
   docker run --dns 8.8.8.8 --dns 8.8.4.4 -p 8050:8050 scrapinghub/splash
   ```

2. **启动爬虫**：

   使用 Scrapy 命令启动爬虫。

   ```bash
   scrapy crawl starbucks 
   ```
   
   启动后程序会打印当前运行环境：
   ```
   Scrapy 2.11.0 started (bot: seventeen_k)
   2024-12-31 09:49:18 [scrapy.utils.log] INFO: Versions: lxml 5.3.0.0, libxml2 2.11.7, cssselect 1.2.0, parsel 1.9.1, w3lib 2.2.1, Twisted 22.10.0, Python 3.9.21 (main, Dec 11 2024, 16:35:24) [MSC v.1929 64 bit (AMD64)], pyOpenSSL 24.3.0 (OpenSSL 3.4.0 22 Oct 2024), cryptography 44.0.0, Platform Windows-10-10.0.19045-SP0
   ```

### 注意事项

- 由于网站采用动态渲染，所以运行时可能会出现一些问题，比如：

  - 部分章节无法提取，可能是由于 splash 性能原因，可修改代码增加 wait_time 
  - 仅提取了一本书，如需批量提取，需要修改代码，删去 index == 0 的限制条件
  - CrawlSpider 无法正常运行，Scrapy-Splash 存在bug，因此采用基础爬虫框架递归爬取实现，可根据情况修改采用广度优先爬取

---

***2024/12/31 listened by guxinghuahuo***