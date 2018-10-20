# coding: utf-8
# In[ ]:
# 中医美容
# http://www.zghzyw.com/zyrm/mr/list_85_1.html
import requests
import json
from lxml import etree
all_urls = set()
all_urls.update([1, 2, 3])
all_urls

for i in range(1, 521):
    print(f"Page: {i}")
    root_url = f"http://www.zghzyw.com/zyrm/mr/list_85_{i}.html"
    resp = requests.get(root_url)
    print(f"resp:{resp}")
    html = etree.HTML(resp.text)
    print(f"html:{html}")
    all_urls.update(html.xpath('.//div[@class="u-post"]//h3/a/@href'))  #
    print(html.xpath('.//div[@class="u-post"]//h3/a/@href'))
print(len(all_urls))

# 去掉非 html 结尾的字段
union_urls = list(filter(lambda x: str(x).endswith(".html"), all_urls))
len(union_urls)

with open("union_urls.json", "w") as file:
    json.dump(union_urls, file)

import requests
import json
from lxml import etree

with open("union_urls.json", "r") as file:
    union_urls = json.load(file)

content_file = open("content_file.csv", "a", encoding="utf-8-sig")

for idx in range(0, len(union_urls)):
    print(idx)
    resp = requests.get("http://www.zghzyw.com" + union_urls[idx])
    resp.encoding = resp.apparent_encoding
    html = etree.HTML(resp.text)
    title = html.xpath('.//div[@class="m-post"]//h1[@class="post-title"]/text()')
    content = html.xpath('.//div[@class="m-post"]//div[@id="ctrlfscont"]//text()')
    title = title[0] if title else ""
    content = "\n".join(map(lambda x: x.strip(), content))

    # print(title)
    # print(content)
    # all_content.append((title, content))
    content_file.write(title+","+content+"\n")
    # break
    
content_file.close()

