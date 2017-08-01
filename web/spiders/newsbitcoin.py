# -*- coding: utf-8 -*-
import scrapy
from web.spiders.basicspider import BasicSpider
from web.items import WebItem
from scrapy.exceptions import NotConfigured
import time
import datetime


class NewsbitcoinSpider(BasicSpider):
    name = "newsbitcoin"
    start_url = [
        'https://news.bitcoin.com',
        'https://news.bitcoin.com/page/2/',
        'https://news.bitcoin.com/page/3/',
    ]

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url,
                                 method='GET',
                                 cookies=self.settings.get('COOKIES'),
                                 callback=self.parse,
                                 errback=self.errback)

    def parse(self, response):
        link = '//h3[@class="entry-title td-module-title"]/a/@href'

        try:
            urls = response.xpath(link).extract()
            for url in urls:
                yield scrapy.Request(url=url,
                                 method='GET',
                                 callback=self.parsepage,
                                 errback=self.errback)
        except Exception as e:
            self.logger.error('{} error: {}'.format(self.name, e))

    def parsepage(self, response):
        try:
            item = WebItem()
            item['title'] = response.xpath(
                '//h1[@class="entry-title"]/text()').extract()[0]
            item['link'] = response.url
            item['time'] = response.xpath(
                '//*[@class="td-post-date"]/time/text()').extract()[0]
            item['time'] = int(time.mktime(
                time.strptime(item['time'], '%B %d, %Y')))
            item['tag'] = self.mark(response.xpath(
                '//footer/div[1]/ul/li/a/text()').extract())
            item['photo'] = response.xpath('//img[@class="entry-thumb"]/@src').extract()[0]
            item['lang'] = 'en'
            yield item
        except Exception as e:
            self.logger.error('{} error:{} {}'.format(self.name, response.url, e))

    def mark(self, marks):
        tags = []
        if 'Bitcoin' in marks:
            tags = 'bitcoin'
        if 'Ethereum' in marks:
            tags = 'blockchain'
        if 'Blockchain' in marks:
            tags = 'blockchain'
        if not tags:
            return 'digitalcoin'
        else:
            return tags
            