"""
获取免费IP代理
James
20181013
"""
from lxml import etree
import requests

url = "http://lab.crossincode.com/proxy/"
# url = "http://www.ai-start.com/dl2017/"

resp = requests.get(url)
# resp.encoding = resp.apparent_encoding
html = etree.HTML(resp.text)
ip = set()
PROXIES = []
result = html.xpath('//tr/td/text()')
for i in range(0, len(result)):
    if i == 0 or i % 6 == 0:
        temp = {f"ip_port: {result[i]}:{result[i + 1]}, 'user_pass': ''"}
        PROXIES.append(temp)
print(PROXIES)




# import random
# a = random.choice(PROXIES)
# # a = requests.get("http://122.112.248.200:88/getTopRecommends").content
# print(str(a))