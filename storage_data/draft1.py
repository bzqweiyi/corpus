from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
session = HTMLSession()
r = session.get('http://news.medlive.cn/cms.php')
# r = session.get('https://python.org/')

about = r.html.xpath('.//div[@class="center_content_area"]//div/a/text()')
print(about)
# print(r.html.links)  # relavant
# print(r.html.absolute_links)

asession = AsyncHTMLSession()
async def get_pythonorg():
    r = await asession.get('https://python.org/')
    print(r.html.links)


async def get_reddit():
    r = await asession.get('https://reddit.com/')


async def get_google():
    r = await asession.get('https://google.com/')



