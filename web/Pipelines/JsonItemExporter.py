from web.Pipelines.BasicPipeline import BasicPipeline
from scrapy.exporters import JsonItemExporter


class JsonWriterPipeline(BasicPipeline):
    def spider_opened(self, spider):
        file = open('%s_items.json' % spider.name, 'wb')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()
