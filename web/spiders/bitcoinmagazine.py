# -*- coding: utf-8 -*-
import scrapy
from web.spiders.basicspider import BasicSpider
from web.items import WebItem
from scrapy.exceptions import NotConfigured
import time
import datetime


class BitcoinmagazineSpider(BasicSpider):
    name = "bitcoinmagazine"
    start_url = [
        'https://bitcoinmagazine.com/archives/2017/',
    ]

    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(url=url,
                                 method='GET',
                                 cookies=self.settings.get('COOKIES'),
                                 callback=self.parse,
                                 errback=self.errback,)

    def parse(self, response):
        root = '//*[@class="archive-list--card"]'
        link = 'div/a[1]/@href'

        for sel in response.xpath(root):
            url = 'https://bitcoinmagazine.com' + sel.xpath(link).extract()[0]
            if 'guides' in url:
                pass
            else:
                yield scrapy.Request(url=url,
                                     method='GET',
                                     callback=self.parsepage,
                                     errback=self.errback,)

    def parsepage(self, response):
        try:
            item = WebItem()
            item['title'] = response.xpath(
                '//article/div[2]/div[1]/h1/text()').extract()[0]
            item['link'] = response.url
            item['time'] = response.xpath(
                '//*[@id="authorSidebar"]/div/time/text()').extract()[0].strip()
            item['time'] = int(time.mktime(
                time.strptime(item['time'], '%b %d, %Y')))
            item['tag'] = response.xpath(
                '//*[@id="authorSidebar"]/div/div[1]/a/text()').extract()
            if item['tag'] == ['/ ETHEREUM']:
                item['tag'] = 'blockchain'
            elif item['tag'] == ['/ BLOCKCHAIN']:
                item['tag'] = 'blockchain'
            else:
                item['tag'] = 'digitalcoin'
            item['photo'] = response.xpath(
                '//img/@src').extract()[0]
            item['lang'] = 'en'
            yield item
        except IndexError as e:
            try:
                item = WebItem()
                item['title'] = response.xpath(
                    '//article/div[1]/div[1]/h1/text()').extract()[0]
                item['link'] = response.url
                item['time'] = response.xpath(
                    '//*[@id="authorSidebar"]/div/time/text()').extract()[0].strip()
                item['time'] = int(time.mktime(
                    time.strptime(item['time'], '%b %d, %Y')))
                item['tag'] = 'digitalcoin'
                item['photo'] = response.xpath(
                    '//img/@src').extract()[0]
                item['lang'] = 'en'
                yield item
            except Exception as e:
                self.logger.error('{} error:{} {}'.format(
                    self.name, response.url, e))
        except Exception as e:
            self.logger.error('{} error:{} {}'.format(
                self.name, response.url, e))
