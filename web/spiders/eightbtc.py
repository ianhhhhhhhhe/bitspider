# -*- coding: utf-8 -*-
import scrapy
from web.spiders.basicspider import BasicSpider
from web.items import WebItem
import time
import datetime


class EightbtcSpider(BasicSpider):
    name = "eightbtc"
    start_url = [
        'http://www.8btc.com/bitcoin',
        'http://www.8btc.com/jzb',
        'http://www.8btc.com/blockchain',
    ]

    def start_requests(self):
        yield scrapy.Request(url='http://www.8btc.com/bitcoin',
                             method='GET',
                             callback=self.parsebitcoin,
                             errback=self.errback,)
        yield scrapy.Request(url='http://www.8btc.com/jzb',
                             method='GET',
                             callback=self.parsejzb,
                             errback=self.errback,)
        yield scrapy.Request(url='http://www.8btc.com/blockchain',
                             method='GET',
                             callback=self.parseblockchain,
                             errback=self.errback,)


    def parsebitcoin(self, response):
        root = '//*[@class="article-content clearfix"]'
        title = 'div/a/@title'
        link = 'div/a/@href'
        ptime = 'div/span/text()'

        photos = []
        for sel in response.xpath('//*[@class="thumb animated flipInY"]'):
            photos.append(sel.xpath('a/span/img/@src').extract()[0])

        for sel in response.xpath(root):
            try:
                item = WebItem()
                item['title'] = sel.xpath(title).extract()[0]
                item['link'] = sel.xpath(link).extract()[0]
                ntime = sel.xpath(ptime).extract()[0]
                try:
                    ntime = int(time.mktime(
                        time.strptime(ntime, '%Y-%m-%d %H:%M')))
                except:
                    ntime = int(time.mktime(
                        time.strptime(ntime, '%Y-%m-%d')))
                item['time'] = ntime
                item['tag'] = 'bitcoin'
                item['photo'] = photos[0]
                del(photos[0])
                item['lang'] = 'cn'
                yield item
            except Exception as e:
                self.logger.error('{} error:{} {}'.format(
                    self.name, response.url, e))

    def parsejzb(self, response):
        root = '//*[@class="article-content clearfix"]'
        title = 'div/a/@title'
        link = 'div/a/@href'
        ptime = 'div/span/text()'

        photos = []
        for sel in response.xpath('//*[@class="thumb-img animated flipInY"]'):
            photos.append(sel.xpath('a/img/@src').extract()[0])

        for sel in response.xpath(root):
            try:
                item = WebItem()
                item['title'] = sel.xpath(title).extract()[0]
                item['link'] = sel.xpath(link).extract()[0]
                ntime = sel.xpath(ptime).extract()[0]
                try:
                    ntime = int(time.mktime(
                        time.strptime(ntime, '%Y-%m-%d %H:%M')))
                except:
                    ntime = int(time.mktime(
                        time.strptime(ntime, '%Y-%m-%d')))
                item['time'] = ntime
                item['tag'] = 'digitalcoin'
                item['photo'] = photos[0]
                del(photos[0])
                item['lang'] = 'cn'
                yield item
            except Exception as e:
                self.logger.warning('{} error:{} {}'.format(
                    self.name, response.url, e))

    def parseblockchain(self, response):
        root = '//*[@class="article-content clearfix"]'
        title = 'div/a/@title'
        link = 'div/a/@href'
        ptime = 'div/span/text()'

        # photos = response.xpath('//img/@data-original').extract()
        photos = []
        for sel in response.xpath('//*[@class="thumb-img animated flipInY"]'):
            photos.append(sel.xpath('a/img/@data-original').extract()[0])

        for sel in response.xpath(root):
            try:
                item = WebItem()
                item['title'] = sel.xpath(title).extract()[0]
                item['link'] = sel.xpath(link).extract()[0]
                ntime = sel.xpath(ptime).extract()[0]
                try:
                    ntime = int(time.mktime(
                        time.strptime(ntime, '%Y-%m-%d %H:%M')))
                except:
                    ntime = int(time.mktime(
                        time.strptime(ntime, '%Y-%m-%d')))
                item['time'] = ntime
                item['tag'] = 'blockchain'
                item['photo'] = photos[0]
                del(photos[0])
                item['lang'] = 'cn'
                yield item
            except Exception as e:
                self.logger.warning('{} error:{} {}'.format(
                    self.name, response.url, e))

