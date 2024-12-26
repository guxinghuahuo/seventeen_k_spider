import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
import random

wait_time = random.uniform(3, 5)

class NovelSpider(Spider):
    name = "novel"
    allowed_domains = ["17k.com"]
    start_urls = ["https://www.17k.com/all/book/2_0_0_0_3_0_1_0_1.html"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': wait_time})

    def parse(self, response):
        """
        处理页面中所有符合规则的链接
        """

        link_extractor = LinkExtractor(allow=r'/book/\d+.html', restrict_xpaths=('//td[@class="td3"]/span/a'))
        links = link_extractor.extract_links(response)
        with open('parse.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)

        print('链接数量：', len(links), links)
        for index, link in enumerate(links):
            headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': link.url
                }
            # 限制一本书
            if index == 0:
                print("限制一本书：", link.url)
                yield SplashRequest(link.url, self.parse_book, args={'wait': wait_time}, headers=headers)
            else:
                return
            

    def parse_book(self, response):
        """
        解析书籍页面
        """
        item = {}
        print('解析书籍：', response.url)
        with open('links.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)
        # 获取书籍信息
        title = response.xpath('//div[@class="Info "]/h1/a/text()').extract_first()
        word_count = response.xpath('//div[@class="BookData"]/p[2]/em/text()').extract_first()
        category = response.xpath('//dl[@id="bookInfo"]/dd/div[2]/table/tbody/tr/td[2]/a/text()').extract_first()
        discription = ''.join(response.xpath('//*[@id="bookInfo"]/dd/div[1]/p/a/text()').extract())
        novel_url = response.url
        chapters_url = response.xpath('//dt[@class="read"]/a/@href').extract_first()

        print('title:', title)
        print('word_count:', word_count)
        print('category:', category)
        print('discription:', discription)
        print('novel_url:', novel_url)
        print('chapters_url:', chapters_url)

        # 存储信息
        # item['title'] = title
        # item['word_count'] = word_count
        # item['category'] = category
        # item['discription'] = discription
        # item['novel_url'] = novel_url
        # item['chapters_url'] = chapters_url

        # 返回抓取的书籍信息
        yield item

    #     # 继续抓取章节页面
    #     if chapters_url:
    #         yield SplashRequest(chapters_url, self.parse_chapter, args={'wait': 2})

    # def parse_chapter(self, response):
    #     """
    #     解析章节页面
    #     """
    #     item = {}
    #     print('解析章节：', response.url)

    #     # 获取章节内容
    #     chapter_title = response.xpath('//h1[@class="chapter-title"]/text()').extract_first()
    #     chapter_content = ''.join(response.xpath('//div[@class="chapter-content"]/p/text()').extract())

    #     # 存储信息
    #     item['chapter_title'] = chapter_title
    #     item['chapter_content'] = chapter_content
    #     item['chapter_url'] = response.url

    #     # 返回抓取的章节信息
    #     yield item
