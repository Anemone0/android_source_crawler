# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import os
import json
import settings


# class SrcCrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item
class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open(os.path.join(settings.ITEMS_STORE, 'items.json'), 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class GitFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        scrapy_pipline_path = super(GitFilePipeline, self).file_path(request, response, info)
        _dir, _file = scrapy_pipline_path.split("/")
        return os.path.join(_file[:1], _file)
