# -*- coding: utf-8 -*-
import scrapy
from web.spiders.basicspider import BasicSpider
from web.items import WebItem
from scrapy.exceptions import NotConfigured
import time
import datetime


class CoindeskSpider(BasicSpider):
    name = "coindesk"
    start_url = [
        'http://www.coindesk.com/category/technology-news/bitcoin/',
        'http://www.coindesk.com/category/technology-news/ethereum-technology-news/',
        'http://www.coindesk.com/category/technology-news/other-public-protocols/',
        'http://www.coindesk.com/category/technology-news/distributed-ledger-technology/',
        'http://www.coindesk.com/category/technology-news/reviews-technology-news/',
    ]

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url,
                                 method='GET',
                                 cookies=self.settings.get('COOKIES'),
                                 callback=self.parse,
                                 errback=self.errback,)

    def parse(self, response):
        root = '//*[@class="post-info"]'
        title = 'h3/a/text()'
        link = 'h3/a/@href'
        ptime = 'p[1]/time/text()'

        photos = response.xpath('//*[@class="picture"]/a/img/@src').extract()

        for sel in response.xpath(root):
            try:
                item = WebItem()
                item['title'] = sel.xpath(title).extract()[0]
                item['link'] = sel.xpath(link).extract()[0]
                ntime = sel.xpath(ptime).extract()[0].strip()
                ntime = int(time.mktime(
                    time.strptime(ntime, '%b %d, %Y at %H:%M')))
                item['time'] = ntime
                if item['link'][0:4] != 'http':
                    item['link'] = response.url + item['link']
                item['tag'] = self.mark(response.url.split('/')[-2])
                item['photo'] = photos[0]
                del(photos[0])
                item['lang'] = 'en'
                yield item
            except Exception as e:
                self.logger.error('{} error:{} {}'.format(self.name, response.url, e))
    
    def mark(self, tag):
        if tag =='bitcoin':
            return tag
        elif tag == 'ethereum-technology-news':
            return 'blockchain'
        else :
            return 'digitalcoin'
