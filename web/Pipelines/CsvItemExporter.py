from web.Pipelines.BasicPipeline import BasicPipeline
from scrapy.exporters import CsvItemExporter


class CsvWriterPipeline(BasicPipeline):
    def spider_opened(self, spider):
        file = open('%s_items.csv' % spider.name, 'wb')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()
