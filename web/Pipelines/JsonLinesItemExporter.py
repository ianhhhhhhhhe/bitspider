from web.Pipelines.BasicPipeline import BasicPipeline
from scrapy.exporters import JsonLinesItemExporter


class JsonLinesWriterPipeline(BasicPipeline):
    def spider_opened(self, spider):
        file = open('%s_items.jl' % spider.name, 'wb')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()
