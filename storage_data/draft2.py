from lxml import etree
import requests
import time


def start(m=0, n=11):
    # url = "http://news.medlive.cn/cms.php"
    url = "http://case.medlive.cn/cms.php"

    header_data = {
        "Accept": "application/json, text/javascript, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "98",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "ymt_pk_id=997d963f1e6dca99; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221668098fc7c171-074f2c0d833c52-65547628-2073600-1668098fc7db6b%22%2C%22%24device_id%22%3A%221668098fc7c171-074f2c0d833c52-65547628-2073600-1668098fc7db6b%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%7D; ymtinfo=eyJ1aWQiOiIwIiwicmVzb3VyY2UiOiIiLCJhcHBfbmFtZSI6IiIsImV4dF92ZXJzaW9uIjoiMSJ9; Hm_lvt_62d92d99f7c1e7a31a11759de376479f=1539755802,1539829371,1539853142,1539911536; _pk_ref.3.a971=%5B%22%22%2C%22%22%2C1539911536%2C%22http%3A%2F%2Fwww.medlive.cn%2F%22%5D; _pk_ses.3.a971=*; PHPSESSID=emltgcmtpmqrpaufthtlr158q1; Hm_lpvt_62d92d99f7c1e7a31a11759de376479f=1539912088; _pk_id.3.a971=997d963f1e6dca99.1539755802.10.1539912088.1539853142.",
        "Host": "case.medlive.cn",
        "Origin": "http://case.medlive.cn",
        "Referer": "http://case.medlive.cn/all/case-case/index.html?ver=branch",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3510.2 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest", }

    form = {
        "submit_type": "ajax",
        "ac": "case_classical_branch",
        "div_type": "all",
        "model_type": "case",
        "cat_type": "case", }

    s = requests.Session()
    for i in range(m, n):
        form["page"] = i
        req = requests.Request("post", url, headers=header_data, data=form)
        prepped = req.prepare()
        resp = s.send(prepped)

        if resp.status_code == 200:
            tree = etree.HTML(resp.text)
            ex_urls = tree.xpath('.//a/@href')
            ex_urls = set([*map(lambda x: x.replace("\\", "").replace('"', ""), ex_urls)])
            with open("d:/urls_case.csv", "a") as file:
                file.write("\n".join(ex_urls) + "\n")
        print(f"response i:{i}")
        time.sleep(0.1)

# http://case.medlive.cn/cms.php
# total page number is 1284.
start(m=0, n=1284)