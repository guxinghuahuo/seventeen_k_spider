import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
import random
from seventeen_k.utils import headers

wait_time = random.uniform(3, 5)
domain = 'https://www.17k.com'

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
        with open('books.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)

        # print('链接数量：', len(links), links)
        for index, link in enumerate(links):
            header = headers.get_headers(link.url)
            # 限制一本书
            if index == 0:
                print("限制一本书：", link.url)
                yield SplashRequest(link.url, self.parse_book, args={'wait': wait_time}, headers=header)
            else:
                return
            

    def parse_book(self, response):
        """
        解析书籍页面
        """
        item = {}
        print('解析书籍：', response.url)
        with open('book.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)
        # 获取书籍信息
        title = response.xpath('//div[@class="Info "]/h1/a/text()').extract_first()
        word_count = response.xpath('//div[@class="BookData"]/p[2]/em/text()').extract_first()
        category = response.xpath('//dl[@id="bookInfo"]/dd/div[2]/table/tbody/tr/td[2]/a/text()').extract_first()
        discription = ''.join(response.xpath('//*[@id="bookInfo"]/dd/div[1]/p/a/text()').extract())
        novel_url = response.url
        chapters_url = domain + response.xpath('//dt[@class="read"]/a/@href').extract_first()

        print('title:', title)
        print('word_count:', word_count)
        print('category:', category)
        print('discription:', discription)
        print('novel_url:', novel_url)
        print('chapters_url:', chapters_url)

        header = headers.get_headers(chapters_url)

        yield SplashRequest(chapters_url, self.parse_chapter, args={'wait': wait_time}, headers=header)



    def parse_chapter(self, response):
        """
        解析章节页面
        """
        item = {}
        print('解析章节：', response.url)

        # # 存储信息
        # item['chapter_title'] = chapter_title
        # item['chapter_content'] = chapter_content
        # item['chapter_url'] = response.url

        link_extractor = LinkExtractor(allow=r'/chapter/\d+/\d+.html', restrict_xpaths=('//dl[@class="Volume"]/dd/a'))
        links = link_extractor.extract_links(response)
        with open('charpters.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)

        # print('链接数量：', len(links), links)
        for index, link in enumerate(links):
            header = headers.get_headers(link.url)
            # 限制一个章节
            if index == 0:
                print("限制一个章节：", link.url)
                yield SplashRequest(link.url, self.parse_chapter_content, args={'wait': wait_time}, headers=header)
            else:
                return

        
    def parse_chapter_content(self, response):
        """
        解析章节内容页面
        """
        item = {}
        print('解析章节内容：', response.url)
        with open('charpter_content.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)

        # # 获取章节内容
        chapter_title = response.xpath('//div[@class="readAreaBox content"]/h1/text()').extract()
        chapter_content = '\n'.join(response.xpath('//div[@class="readAreaBox content"]/div[@class="p"]/p/text()').extract())

        # # 存储信息
        # item['chapter_title'] = chapter_title
        # item['chapter_content'] = chapter_content
        # item['chapter_url'] = response.url

        print('chapter_title:', chapter_title)
        print('chapter_content:', chapter_content)

        yield item