# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeventeenKItem(scrapy.Item):
    category = scrapy.Field()
    book_name = scrapy.Field()
    book_nums = scrapy.Field()
    description = scrapy.Field()
    book_url = scrapy.Field()
    chapter_url = scrapy.Field()
    pass


class ChapterItem(scrapy.Item):
    chapter_list = scrapy.Field()


class ContentItem(scrapy.Item):
    content = scrapy.Field()
    chapter_detail_url = scrapy.Field()

    