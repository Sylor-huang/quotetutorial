# -*- coding: utf-8 -*-
import scrapy

from quotetutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"  #指定spider的名称
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()
            #scrapy的spider特有语法，输出text属性里的text文档内容。extract提取前面函数里的全部内容，extract_first()提取前面函数里的第一条内容。
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next) #获取目标路径的绝对地址。
        yield scrapy.Request(url=url,callback=self.parse) #callback表示回调函数的意思，即获得response后，再由callback表示由哪个函数处理。本案例表示递归调用，自己调用自己。实现翻页效果

