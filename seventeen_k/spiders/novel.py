from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class NovelSpider(CrawlSpider):
    name = "novel"
    allowed_domains = ["17k.com"]
    start_urls = ["https://www.17k.com/all/book/2_0_0_0_3_0_1_0_1.html"]

    rules = (
        # 提取目录页的链接
        Rule(
            LinkExtractor(allow=r'/book/\d+.html', restrict_xpaths=('//td[@class="td3"]/span/a')), 
            callback='parse_book',
            follow=True,
            process_links="process_booklink"
        ),
        # 匹配章节目录的url

    )

    def process_booklink(self,links):
        print('链接数量：', len(links), links)
        for index, link in enumerate(links):
            # 限制一本书
            if index == 0:
                print("限制一本书：", link.url)
                yield link
            else:
                return

    def parse_book(self, response):
        item = {}
        print('解析书籍：', response.url)
        # 书名
        title = response.xpath('//div[@class="Info"]/h1/a/text()').extract_first()
        # 字数
        word_count = response.xpath('//div[@class="BookData"]/p[2]/em/text()').extract_first()
        # 分类
        category = response.xpath('//dl[@id="bookInfo"]/dd/div[2]/table/tbody/tr/td[2]/a/text()').extract_first()
        # 概述
        discription = ''.join(response.xpath('//*[@id="bookInfo"]/dd/div[1]/p/a/text()').extract())
        # 小说链接
        novel_url = response.url
        # 小说章节
        chapters_url = response.xpath('//dt[@class="read"]/a/@href').extract_first()
        print(title, word_count, category, discription, novel_url, chapters_url)
        return item
    
