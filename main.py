import logging

from twisted.internet import reactor, defer

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from web.spiders.newsbitcoin import NewsbitcoinSpider
from web.spiders.cointelegraph import CointelegraphSpider
from web.spiders.coindesk import CoindeskSpider
from web.spiders.bitcoinmagazine import BitcoinmagazineSpider
from web.spiders.newsbtc import NewsbtcSpider
from web.spiders.cryptocoinsnews import CryptocoinsnewsSpider
from web.spiders.eightbtc import EightbtcSpider


def main():
    configure_logging(get_project_settings())
    runner = CrawlerRunner(get_project_settings())

    @defer.inlineCallbacks
    def crawl():
        # yield runner.crawl(NewsbtcSpider)
        yield runner.crawl(NewsbitcoinSpider)
        yield runner.crawl(EightbtcSpider)
        yield runner.crawl(CryptocoinsnewsSpider)
        yield runner.crawl(CointelegraphSpider)
        yield runner.crawl(CoindeskSpider)
        yield runner.crawl(BitcoinmagazineSpider)
        reactor.stop()

    crawl()
    reactor.run()

if __name__ == '__main__':
    main()