#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/6/13'

__QQ__ = '376205871'

"""

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import ArticlespiderItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http import Request
import urllib.parse
from math import floor
import re
import time
import random
from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)


class Ask999Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'zghzyw'
    allowed_domains = ['www.zghzyw.com/']
    start_urls = "http://www.zghzyw.com/zyrm/mr/"
    redis_key = 'zghzyw:start_urls'
    # start_urls = [
    # 'http://www.999ask.com/list/gaoxuezhi/all/2.html' # 高血脂
    #     ]
    rules = (
        Rule(LinkExtractor(allow=r"http://www.zghzyw.com/\d+/$"), callback="parse", follow=False),
        # Rule(LinkExtractor(allow=()), callback="parse_detail_mongo", follow=False),
    )

    def parse(self, response):
        for i in range(1, 521):
            nextpage = f"http://www.zghzyw.com/zyrm/mr/list_85_{i}.html"
            # href = "http://www.zghzyw.com/zyrm/mr/list_85_1.html"  # 美容
            print(f"nextpage, {nextpage}")
            try:
                time.sleep(random.uniform(1.1, 2))
                yield Request(nextpage, callback=self.parse_next, dont_filter=True)
            except Exception as e:
                print(e)


    def parse_next(self, response):
        # nextpath = '//*[@id="main"]/div[1]/div/div[' + str(i) + "]" + "/div[1]/h3/a/@href"
        # url = response.xpath(nextpath)
        urls = response.xpath('.//div[@class="u-post"]//h3/a/@href').extract()
        for url in urls:
            newpath = "http://www.zghzyw.com" + url
            print(f"newpath,{newpath}")
            yield Request(newpath, callback=self.parse_detail_mongo, dont_filter=True)


    def parse_detail_mongo(self, response):
        item = ArticlespiderItem()
        try:
            # time.sleep(random.uniform(1.1, 5))
            # 获取文章url & title
            item['url'] = response.url
            print("url: ", item['url'])
            # response.xpath('//div[@class="u-post"]').extract()
            try:
                title = response.xpath('.//div[@class="m-post"]//h1[@class="post-title"]/text()').extract()[0]
                title = self.filter_tags_blank(title)
            except Exception as e:
                title = ""
                print("title :", e)
            try:
                # 获取文章内容" //*[@id="content"]/div/div[3]/text()"
                content = "".join(response.xpath('.//div[@class="m-post"]//div[@id="ctrlfscont"]//text()').extract())
                content = self.filter_tags_blank(content)
                # position = response.xpath('//body/div/div/div/div/b/text()').extract()[0]
                # category0 = response.xpath('//body/div/div/div/div/a/text()').extract()[0]
                # category1 = response.xpath('//body/div/div/div/div/a/text()').extract()[1]
                # category = position + ": >" + category0 + ">" + category1
                # category = self.filter_tags_blank(title)
                # print("category :", category)
            except Exception as e:
                content = ""
                print("content :", e)
            item['title'] = title
            item['content'] = content
            print(f"title: ,{title}")
            print(f"descText, {content}")
            # item['category'] = category
            yield item
        except Exception as e:
            print("Error2 :", e)
            logger.info("匹配信息出错。错误原因:")
            logger.info(e)


    """
    去掉html标签和空格
    """
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())
