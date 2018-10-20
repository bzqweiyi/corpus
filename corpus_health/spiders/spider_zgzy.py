#!/usr/bin/env python3.6

# -*- coding: utf-8 -*-

"""
__author__ = 'jasonqu'

__date__ = '2018/5/29'

__QQ__ = '376205871'

"""
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from corpus_health.items import HealthItem
from scrapy_redis.spiders import RedisCrawlSpider
import urllib.parse
from math import floor
from scrapy.http import Request
import re

from corpus_health.Util.LogHandler import LogHandler
logger = LogHandler(__name__, stream=True)


class Ask120Spider(RedisCrawlSpider):
    handle_httpstatus_list = [404, 403, 500]
    name = 'zhzyw'
    allowed_domains = ['www.zhzyw.com']
    start_urls = "https://www.zhzyw.com"
    #     ]
    redis_key = 'zhzyw:start_urls'
    rules = (
        Rule(LinkExtractor(allow=r"//www.zhzyw.com/list/bianmi/all/\d+/$"), callback="parse", follow=False),
        #Rule(LinkExtractor(allow=r"http://www.120ask.com/question/\d+\.htm$"), callback="parse_detail_mongo", follow=False),
    )
    def parse(self, response):
        #href = "https://www.zhzyw.com/zyxx/mymy/" #古今名医
        #href="https://www.zhzyw.com/zyxx/ycsc/" #药材市场
        #href="https://www.zhzyw.com/zycs/zyjs/" ###中医简史
        #href="https://www.zhzyw.com/zyxx/zysj/" #中医书籍
        #href="https://www.zhzyw.com/zyxx/zyxw/" #中医新闻
        #href="https://www.zhzyw.com/zycs/wwwq/" #中医诊断
        #href="https://www.zhzyw.com/zycs/zycs/" #中药常识
        #href="https://www.zhzyw.com/zycs/zycd/" #中药词典
        #href="https://www.zhzyw.com/zycs/zytp/" #中医图谱
        #href="https://www.zhzyw.com/zycs/zywh/" #中医文化
        #href="https://www.zhzyw.com/zyts/pfmf/" #偏方秘方
        #href="https://www.zhzyw.com/zyts/zybg/" #中医拔罐
        #href="https://www.zhzyw.com/zyts/zygy/" #中医膏药
        #href="https://www.zhzyw.com/zyts/zygs/" #中医刮痧
        #href="https://www.zhzyw.com/zyts/zyhl/" #中医火疗
        #href="https://www.zhzyw.com/zyts/zyqg/" #中医气功
        #href="https://www.zhzyw.com/zyts/zytn/" #中医推拿
        #href="https://www.zhzyw.com/zyts/zyyc/" #中医药茶
        #href="https://www.zhzyw.com/zyts/zyyj/" #中医药酒
        #href="https://www.zhzyw.com/zyts/zyyy/" #中医药浴
        #href="https://www.zhzyw.com/zyts/zyzj/" #中医针灸
        #href="https://www.zhzyw.com/zyts/zrlf/" #自然疗法
        #href="https://www.zhzyw.com/zybj/zyfx/" #中医丰胸
        #href="https://www.zhzyw.com/zybj/zyjf/" #中医减肥
        #href="https://www.zhzyw.com/zybj/zymr/" #中医美容
        #href="https://www.zhzyw.com/zybj/lnbj/" #老年保健
        #href="https://www.zhzyw.com/zybj/zyye/" #中医育儿
        #href="https://www.zhzyw.com/zybj/nxbj/" #男性保健
        #href="https://www.zhzyw.com/zybj/nvxbj/" #女性保健
        href="https://www.zhzyw.com/zybj/zyys/" #中医养生
        print(href)
        yield Request(href, callback=self.parese_next, dont_filter=True)
    
    def parese_next(self, response):
        hxs = response.xpath('//body/div/div/div/div/h3/a').extract() #tbody/trtd/span/a
        for nextItem in hxs:
            pref = '<a href=\"'
            begin = len(pref)
            end = nextItem.index("\">")
            href = self.start_urls + nextItem[begin:end]
            i = 1
            while (i < 100):
                hrefT = "index"
                if i > 1: hrefT = hrefT + "_"+ str(i)
                hrefT = hrefT + ".html"
                i = i + 1      
                print(href+hrefT)
                yield Request(href+hrefT, callback=self.parese_next_next,dont_filter=True)
                    
    def parese_next_next(self, response):
        hxs = response.xpath('//body/div/div/div/ul/li/a').extract() #tbody/trtd/span/a
        print(hxs)
        for nextItem in hxs:
            pref = '<a href=\"'
            begin = len(pref)
            end = nextItem.index(".html")
            href = self.start_urls + nextItem[begin:end+5]
            print(href)
            if href != None: yield Request(href, callback=self.parse_detail_mongo,dont_filter=True)
            
    def parse_detail_mongo(self, response):
       item = HealthItem()
       try:
            item['url'] = response.url
            
            category = response.xpath('//div[@id="wzdh"]').extract()[0]
            categoryText = self.filter_tags_blank(category)
            item['category'] = categoryText
            
            title = response.xpath('//h1').extract()[0]
            titleTxt = self.filter_tags_blank(title)
            item['title'] = titleTxt
            
            desc = response.xpath('//div[@class="daodu"]').extract()[0]
            descText = self.filter_tags_blank(desc)
            item['desc'] = descText
            
            content = response.xpath('//div[@class="webnr"]').extract()[0]
            contentText = self.filter_tags_blank(content)
            item['content'] = contentText
            
            print(item)
            yield item
       except Exception as e:
            print(e)
            logger.info("匹配信息出错。错误原因:")
            logger.info(e)

    """
    去掉html标签和空格
    """
    def filter_tags_blank(self, str):
        p = re.compile('<[^>]+>').sub("", str)
        return "".join(p.split())
