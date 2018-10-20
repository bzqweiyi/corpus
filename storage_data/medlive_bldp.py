# -*- encoding:utf-8 -*-
"""
# James
# 20181018
# TODO: add itertools
"""

from lxml import etree
import requests
import datetime
from itertools import islice
import time
import csv


def spider_mdelive():
    with open("D:/urls_ynxw.csv", "r") as urls:
        count = 33623
        articles = []
        for temp_url in islice(urls, 33623, None):
            url = f"http://news.medlive.cn" + temp_url
            try:
                resp = requests.get(url)
                record_time = time.time()
                while resp.status_code != 200:
                    current_time = time.time()
                    delt_time = current_time - record_time
                    resp = requests.get(url)
                    time.sleep(10)
                    ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{ctime} delt_time, {delt_time} s")
                    if delt_time > 4000:
                        break
            except Exception as e:
                print(e)
            resp.encoding = resp.apparent_encoding
            html = etree.HTML(resp.text)
            title = "".join(html.xpath('.//div[@id="content"]//div/h1/text()'))
            content = "".join(html.xpath('.//div[@class="content_body"]//text()'))
            articles.append([title, content])
            count += 1
            ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")
            print(f"{ctime} count:{count} ,title:{title},\nurl:{url}")
            time.sleep(0.1)
            save_to_csv(articles)
            ctime1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")
            print(f"{ctime1} saved {count} into local file." + "\n")
            articles = []


def save_to_csv(articles):
    with open("D:/医脉通_业内新闻.csv", "a", newline='', encoding="utf_8_sig") as file:
        writer = csv.writer(file)
        for row in articles:
            writer.writerow(row)


if __name__ == "__main__":
    try:
        spider_mdelive()
    except Exception as e:
        print(e)