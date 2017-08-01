# -*- coding: utf-8 -*-
import scrapy
from web.spiders.basicspider import BasicSpider
from web.items import WebItem
from scrapy.exceptions import NotConfigured
import time
import datetime


class CointelegraphSpider(BasicSpider):
    name = "cointelegraph"
    start_url = [
        #'https://cointelegraph.com',
        'https://cointelegraph.com/tags/bitcoin',
        'https://cointelegraph.com/tags/ethereum',
        'https://cointelegraph.com/tags/altcoin',
        'https://cointelegraph.com/tags/blockchain',
        'https://cointelegraph.com/tags/bitcoin-regulation',
        'https://cointelegraph.com/tags/bitcoin-scams'
    ]

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url,
                                 method='GET',
                                 cookies=self.settings.get('COOKIES'),
                                 callback=self.parse,
                                 errback=self.errback)

    def parse(self, response):
        print(response)
        root = '//*[@id="recent"]/div'
        title = 'figure[2]/h2/a/text()'
        link = 'figure[2]/h2/a/@href'
        ptime = 'figure[2]/div[1]/span[1]/text()'
        photo = 'figure[1]/div[1]/a/div/img/@src'

        for sel in response.xpath(root):
            try:
                item = WebItem()
                item['title'] = sel.xpath(title).extract()[0].strip()
                item['link'] = sel.xpath(link).extract()[0]
                ntime = sel.xpath(ptime).extract()[0].strip()
                if ntime[-3:] == 'AGO':
                    ntime = int(time.mktime(time.strptime(
                        datetime.datetime.now().strftime('%Y %m %d'), '%Y %m %d')))
                else:
                    ntime = int(time.mktime(
                        time.strptime(ntime, '%b %d, %Y')))
                item['time'] = ntime
                if item['link'][0:4] != 'http':
                    item['link'] = response.url + item['link']
                item['time'] = item['time']
                item['tag'] = self.mark(response.url.split('/')[-1])
                item['photo'] = sel.xpath(photo).extract()[0]
                item['lang'] = 'en'
                yield item
            except Exception as e:
                self.logger.error('{} error:{} {}'.format(self.name, response.url, e))

    def mark(self, tag):
        if tag == 'bitcoin':
            return tag
        elif tag == 'ethereum':
            return 'blockchain'
        else:
            return 'digitalcoin'
