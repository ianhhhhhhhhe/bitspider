# -*- coding: utf-8 -*-
import scrapy
from web.spiders.basicspider import BasicSpider
from web.items import WebItem
from scrapy.exceptions import NotConfigured
import time
import datetime


class NewsbtcSpider(BasicSpider):
    name = "newsbtc"
    start_url = [
        'https://www.newsbtc.com/post-view/',
        'https://www.newsbtc.com/post-view/page/2/',
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
        root = '//*[@id="page-body"]/div[1]/div/div/article'
        title = 'div[2]/h2/a/text()'
        link = 'div[2]/h2/a/@href'
        ptime = 'div[2]/div[1]/span/text()'

        for sel in response.xpath(root):
            try:
                item = WebItem()
                item['title'] = sel.xpath(title).extract()[0]
                item['link'] = sel.xpath(link).extract()[0]
                ntime = sel.xpath(ptime).extract()[0]
                ntime = ntime.replace('th', '').replace('nd','').replace('st', '')
                ntime = datetime.datetime.fromtimestamp(time.mktime(
                    time.strptime(ntime, '%B %d, %Y'))).strftime('%Y-%m-%d')
                item['time'] = ntime
                if item['link'][0:4] != 'http':
                    item['link'] = response.url + item['link']
                item['lang'] = 'en'
                yield item
            except Exception as e:
                self.logger.error('{} error:{} {}'.format(self.name, response.url, e))
