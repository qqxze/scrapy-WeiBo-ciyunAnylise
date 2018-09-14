# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.exporters import JsonItemExporter


class WeiboluhanPipeline(object):
    def process_item(self, item, spider):
        return item

class WithText(object):
    # def __init__(self):
    #     self.file = codecs.open('comment.txt', 'w', encoding="utf-8")
    def process_item (self, item, spider):
        self.file = codecs.open('comment.txt', 'a', encoding="utf-8")
        print(item['comment'])
        self.file.write(item['comment'])
        return item
    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipleline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()