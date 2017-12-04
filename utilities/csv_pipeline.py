
from scrapy.exporters import CsvItemExporter


class CsvPipeline(object):
    def __init__(self, category_name):
        self.file = open('../utilities/bin/output/prodirect_running.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def create_valid_csv(self, item):
        for key, value in item.items():
            is_string = (isinstance(value, basestring))
            if is_string and ("," in value.encode('utf-8')):
                item[key] = "\"" + value + "\""

