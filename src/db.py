# encoding:utf-8
__author__ = 'youxiangyang'
from feedback import Feedback
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import sys
import re

keyword = sys.argv[1]
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language': 'zh-cn',
    'Cache-Control': 'max-age=0',
    'Host': 'm.douban.com',
    'DNT': '1'
}
request = urllib.request.Request("https://m.douban.com/search?type=1002&query=" + urllib.parse.quote(keyword), None, headers)
response = urllib.request.urlopen(request)

html = response.read()
patten1 = re.compile(r'(\s\s+)|\n')
html = re.sub(patten1, ' ', html.decode('utf-8'));
find_re = re.compile(
    r'<li>\s<a href="(.+?)">\s<img src=".+?".+?<div class="subject-info">\s<span class="subject-title">(.+?)</span>.+?<p class="rating".+?<span>(.+?)</span>',
    re.DOTALL)

fb = Feedback()
for x in find_re.findall(html):
    link = "https://movie.douban.com" + x[0][6:]  # 链接
    title = x[1]  # 片名 包含别名
    # content = x[2]  # 简介
    rating = x[2].strip()  # 评价
    # rate_count = x[4]  # 评价数
    try:
        rateNum = str(int(float(rating)))
        halfRate = int((float(rating) + 0.5) / 2)
    except (TypeError, ValueError):
        rateNum = 'unknow'
        halfRate = 0
    fb.add_item(title,
        subtitle="★★★★★☆☆☆☆☆"[(5 - halfRate) * 3:(10 - halfRate) * 3] + " " + rating,
        arg=link, icon='favicons/' + rateNum + '.png')
print(fb)

