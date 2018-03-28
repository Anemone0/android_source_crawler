#!/usr/bin/env python
# -*- coding=utf-8 -*-
from lxml import etree

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
        # 传递star url
        xpath_star_url = '//a[contains(@aria-label,"starred this repository")]/@href'
        star_url = response.xpath(xpath_star_url).extract()[0]
        yield Request(base_url + star_url, callback=self.parse_repo_stars)

        # 检查item正确性
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

    def check_valid(self, response):
        xpath_files = '//tr[contains(@class,"js-navigation-item")]/td[contains(@class,"content")]/span/a/text()'
        files = response.xpath(xpath_files).extract()
        gradle_files = ["gradlew", "src", "settings.gradle"]
        for each in gradle_files:
            if each not in files:
                return False
        return True

    def parse_repo_stars(self, response):
        """
        获取所有的star用户，返回每个用户的个人stars页面
        :param response:
        :return:
        """
        xpath_developers = '//h3[contains(@class,"follow-list-name")]//a/@href'
        developers_urls = response.xpath(xpath_developers).extract()
        for developer_url in developers_urls:
            yield Request(base_url + developer_url + "?tab=stars", callback=self.parse_developer_stars)

    def parse_developer_stars(self, response):
        """
        获取每一页面的star仓库
        :param response:
        :return:
        """
        languages = ["Java", "Kotlin"]
        # 枚举每一个项目，看语言是java和kotlin的
        xpath_divs = '//div[contains(@class,"col-12 d-block width-full py-4 border-bottom")]'
        xpath_lang = '//span[contains(@itemprop,"programmingLanguage")]/text()'
        xpath_href = '//h3/a/@href'
        for each in response.xpath(xpath_divs).extract():
            xml_selector = etree.HTML(each)
            lang_arr = xml_selector.xpath(xpath_lang)
            if len(lang_arr) == 0:
                continue
            lang = lang_arr[0].replace("\n", "").strip()
            if lang not in languages:
                continue
            repo_url=xml_selector.xpath(xpath_href)[0]
            yield Request(base_url+repo_url, callback=self.parse)


        # 跳转到下一页
        xpath_next = '//a[contains(@class,"next_page")]/@href'
        next_url = response.xpath(xpath_next).extract()
        if len(next_url) >= 1:
            next_url = next_url[0]
            yield Request(base_url + next_url, callback=self.parse_developer_stars)

    def download_repo(self, response):
        file_name = response.url.split('/')[4]
        suffix_dir = file_name[:2]
        os.makedirs(os.path.join(settings.ZIP_DIR, suffix_dir))
        path = os.path.join(settings.ZIP_DIR, suffix_dir, file_name + '.zip')

        with open(path, 'wb') as f:
            f.write(response.body)


if __name__ == '__main__':
    pass
