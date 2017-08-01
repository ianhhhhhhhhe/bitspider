from web.Pipelines.BasicPipeline import BasicPipeline
from scrapy.exporters import XmlItemExporter


class XmlWriterPipeline(BasicPipeline):
    def spider_opened(self, spider):
        file = open('%s_items.xml' % spider.name, 'wb')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()
