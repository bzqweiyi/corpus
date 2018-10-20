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
from scrapy.http import Request
import re
from corpus_health.Util.LogHandler import LogHandler

logger = LogHandler(__name__, stream=True)


class Ask999Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'zyw_jf'
    allowed_domains = ['www.zghzyw.com/']
    start_urls = [
        "http://www.zghzyw.com/zyrm/jf/"
        # "http://www.zghzyw.com/zyrm/fx/"   # 丰胸
        # "http://www.zghzyw.com/qushi"    # 祛湿
    ]
    redis_key = 'zyw:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r"http://www.zghzyw.com/\d+/$"), callback="parse", follow=False),
        # Rule(LinkExtractor(allow=()), callback="parse_detail_mongo", follow=False),
    )


    def parse(self, response):
        page_number = 277
        for i in range(1, page_number):
            nextpage = f"http://www.zghzyw.com/zyrm/jf/list_84_{i}.html"  # 减肥  page_number = 277
            # nextpage = f"http://www.zghzyw.com/zyrm/mr/list_85_{i}.html"  # 丰胸  page_number = 180
            # nextpage = f"http://www.zghzyw.com/zyrm/mr/list_85_{i}.html"  # 美容  page_number = 521
            # nextpage = f"http://www.zghzyw.com/zyfj/yyjj/list_161_{i}.html"  # 用药禁忌  page_number = 3
            # nextpage = f"http://www.zghzyw.com/zyfj/jbfy/list_158_{i}.html"  # 疾病方药  page_number = 14
            # nextpage = f"http://www.zghzyw.com/zylf/ql.html"  # 脐疗 page_number = 2
            # nextpage = f"http://www.zghzyw.com/zylf/zj/list_67_{i}.html"  # 针灸 page_number = 119
            # nextpage = f"http://www.zghzyw.com/zylf/zl/list_68_{i}.html"  # 足疗 page_number = 19
            # nextpage = f"http://www.zghzyw.com/zylf/tn/list_63_{i}.html"  # 推拿 page_number = 88
            # nextpage = f"http://www.zghzyw.com/zylf/qg/list_61_{i}.html"  # 气功 page_number = 24

            # nextpage = f"http://www.zghzyw.com/zylf/nb/list_59_{i}.html"  # 捏背 page_number = 6
            # nextpage = f"http://www.zghzyw.com/zylf/hl/list_57_{i}.html"  # 火疗 page_number = 12
            # nextpage = f"http://www.zghzyw.com/zylf/gs/list_56_{i}.html"  # 刮痧 page_number = 56
            # nextpage = f"http://www.zghzyw.com/zylf/bg/list_53_{i}.html"  # 拔罐 page_number = 46
            # nextpage = f"http://www.zghzyw.com/zylf/dx/list_54_{i}.html"  # 点穴 page_number = 4

            # nextpage = f"http://www.zghzyw.com/zylf/yj/list_65_{i}.html"  # 药酒 page_number = 85
            # nextpage = f"http://www.zghzyw.com/zyfj/pfmf/list_162_{i}.html"  # 偏方妙方 page_number = ？

            # f"http://www.zghzyw.com/qushi/list_{i}.html"        # 祛湿 page_number = 25
            # f"http://www.zghzyw.com/zyrm/fx/list_83_{i}.html"   # 丰胸 page_number = 180
            print(f"nextpage, {nextpage}")
            try:
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
