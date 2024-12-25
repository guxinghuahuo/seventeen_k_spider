from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class NovelSpider(CrawlSpider):
    name = "novel"
    allowed_domains = ["17k.com"]
    start_urls = ["https://www.17k.com/all/book/2_0_0_0_3_0_1_0_1.html"]

    rules = (
        Rule(
            LinkExtractor(allow=r'/book/\d+.html', restrict_xpaths=('//td[@class="td3"]/span/a')), 
            callback='parse_book',
            follow=True,
            process_links="process_booklink"
        ),
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
        
        return item
    
