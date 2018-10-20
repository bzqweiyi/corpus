#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
中国好中医网：祛湿
James
"""

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import ArticlespiderItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy_redis.spiders import Spider
from scrapy.http import Request
from scrapy.http import FormRequest
import requests
import re
from corpus_health.Util.LogHandler import LogHandler

logger = LogHandler(__name__, stream=True)

class Ask999Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'ymt'
    allowed_domains = ['www.medlive.cn/']
    start_urls = "http://news.medlive.cn/all/info-progress/list.html?ver=branch"
        # "http://www.zghzyw.com/zyrm/fx/"   # 丰胸
        # "http://www.zghzyw.com/qushi"    # 祛湿

    redis_key = 'ymt:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r"http://www.medlive.cn/\d+/$"), callback="parse", follow=False),
        # Rule(LinkExtractor(allow=()), callback="parse_detail_mongo", follow=False),
    )

    # def start_requests(self):
    #     url = ""
    #     requests = []
    #     for i in range(0, 100):
    #         formdata = {
    #             "page": str(i),
    #             "submit_type": "ajax",
    #             "ac": "research_branch",
    #             "div_type": "all",
    #             "model_type": "info",
    #             "cat_type": "research"}
    #         request = FormRequest(url, callback=self.parse, formdata=formdata)
    #         requests.append(request)
    #     return requests


    def parse(self, response):
        urls = [
            "http://news.medlive.cn/infect/info-progress/show-149976_171.html",
            "http://news.medlive.cn/heart/info-progress/show-149938_129.html"]
            # f"http://news.medlive.cn/psy/info-progress/show-149946_60.html",
            #     f"http://news.medlive.cn/endocr/info-progress/show-149951_46.html",
            #     f"http://news.medlive.cn/endocr/info-progress/show-149948_46.html",
            #     f"http://news.medlive.cn/imm/info-progress/show-149926_166.html"]
        for url in urls:
            print(f"url, {url}")
            try:
                # meta = {'dont_redirect': False}
                yield Request(url, callback=self.parse_detail_mongo, dont_filter=True)
            except Exception as e:
                print(e)

    # def parse_next(self, response):
    #     # nextpath = '//*[@id="main"]/div[1]/div/div[' + str(i) + "]" + "/div[1]/h3/a/@href"
    #     # url = response.xpath(nextpath)
    #     urls = response.xpath('.//div[@class="u-post"]//h3/a/@href').extract()
    #     for url in urls:
    #         newpath = "http://www.zghzyw.com" + url
    #         print(f"newpath,{newpath}")
    #         yield Request(newpath, callback=self.parse_detail_mongo, dont_filter=True)

    def parse_detail_mongo(self, response):
        item = ArticlespiderItem()
        try:
            # time.sleep(random.uniform(1.1, 5))
            # 获取文章url & title
            item['url'] = response.url
            print("url: ", item['url'])
            # response.xpath('//div[@class="u-post"]').extract()
            try:
                title = response.xpath('.//div[@id="content"]//div/h1/text()').extract()
                title = self.filter_tags_blank(title)
            except Exception as e:
                title = ""
                print("title :", e)
            try:
                # 获取文章内容" //*[@id="content"]/div/div[3]/text()"
                content = "".join(response.xpath('.//div[@id="content"]//div/p/span/text()').extract())
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
