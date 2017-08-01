# -*- coding: utf-8 -*-
import scrapy
from web.spiders.basicspider import BasicSpider
from web.items import WebItem
from scrapy.exceptions import NotConfigured
import time
import datetime


class CryptocoinsnewsSpider(BasicSpider):
    name = "cryptocoinsnews"
    start_url = [
        'https://www.cryptocoinsnews.com/news/',
        'https://www.cryptocoinsnews.com/news/page/2/',
        'https://www.cryptocoinsnews.com/news/page/3/',
    ]

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url,
                                 method='GET',
                                 cookies=self.settings.get('COOKIES'),
                                 callback=self.parse,
                                 errback=self.errback,)

    def parse(self, response):
        print(response)
        root = '//*[@class="grid-wrapper"]/div'
        title = 'div/h3/a/text()'
        link = 'div/h3/a/@href'
        ptime = 'div/div[2]/span[2]/text()'
        tag = 'div/div/a/text()'
        photo = 'a/img/@src'

        for sel in response.xpath(root):
            try:
                item = WebItem()
                item['title'] = sel.xpath(title).extract()[0]
                item['link'] = sel.xpath(link).extract()[0]
                ntime = sel.xpath(ptime).extract()[0]
                ntime = int(time.mktime(
                    time.strptime(ntime , '%d/%m/%Y')))
                item['time'] = ntime
                if item['link'][0:4] != 'http':
                    item['link'] = response.url + item['link']
                item['tag'] = self.mark(sel.xpath(tag).extract())
                item['photo'] = sel.xpath(photo).extract()[0]
                item['lang'] = 'en'
                yield item
            except Exception as e:
                self.logger.error('{} error:{} {}'.format(self.name, response.url, e))

    def mark(self, marks):
        for mark in marks:
            if 'Bitcoin' in mark:
                return 'bitcoin'
            elif 'Ethereum' in mark:
                return 'blockchain'
            elif 'Blockchain' in mark:
                return 'blockchian'                
        return 'digitalcoin'
