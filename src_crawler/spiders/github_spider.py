#!/usr/bin/env python
# -*- coding=utf-8 -*-
from scrapy.spiders import CrawlSpider
import os
import src_crawler.settings as settings
from scrapy.http import Request
from scrapy.selector import Selector
from src_crawler.items import SrcCrawlerItem
import logging

base_url = 'https://github.com'


class GitHubSpider(CrawlSpider):
    name = "github_spider"
    start_urls = ["https://github.com/owncloud/android"]

    def parse(self, response):
        # 传递watch url，star url，fork url

        # 检查item正确性
        # print response.body
        valid = self.check_valid(response)

        if valid:
            xpath_repo_name = '//strong[contains(@itemprop,"name")]/a/@href'
            xpath_download_url = '//a[contains(@data-ga-click,"download")]/@href'
            repo_name = response.xpath(xpath_repo_name).extract()[0]
            zip_url = base_url + response.xpath(xpath_download_url).extract()[0]

            item = SrcCrawlerItem()

            item["name"] = repo_name
            item["url"] = [zip_url]

            yield item
            # yield Request(zip_url, callback=self.download_repo)

    def check_valid(self, response):
        xpath_files = '//tr[contains(@class,"js-navigation-item")]/td[contains(@class,"content")]/span/a/text()'
        files = response.xpath(xpath_files).extract()
        gradle_files = ["gradlew", "src", "settings.gradle"]
        for each in gradle_files:
            if each not in files:
                return False
        return True

    def parse_watch(self, response):
        pass

    def parse_star(self, response):
        pass

    def parse_fork(self, response):
        pass

    def download_repo(self, response):
        file_name = response.url.split('/')[4]
        suffix_dir = file_name[:2]
        os.makedirs(os.path.join(settings.ZIP_DIR, suffix_dir))
        path = os.path.join(settings.ZIP_DIR, suffix_dir, file_name + '.zip')

        with open(path, 'wb') as f:
            f.write(response.body)


if __name__ == '__main__':
    pass
