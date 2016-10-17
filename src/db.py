# encoding:utf-8
__author__ = 'youxiangyang'
from feedback import Feedback
import urllib
import urllib2
import re

keyword = '{query}'
# keyword = '蚁人'
param = {"search_text": keyword}
data = urllib.urlencode(param)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Host': 'movie.douban.com',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
request = urllib2.Request("https://movie.douban.com/subject_search", data, headers)
response = urllib2.urlopen(request)
html = response.read()

patten1 = re.compile(r'(\s\s+)|\n')
html = re.sub(patten1, ' ', html)
patten2 = re.compile(r'(<span style="font-size:12px;">)|</span>')
patten3 = re.compile(r'<div class="star clearfix">\s*?<span class="allstar00"></span>\s*?<span class="pl">')
html = re.sub(patten3, '<div class="star clearfix"> <span class="rating_nums"> </span><span class="pl">', html)
find_re = re.compile(
    r'<a class="nbg.+?<img src="(.+?)".+?<div class="pl2">.+?<a href="(.+?)".+?>(.+?)</a>.+?<p class="pl">(.+?)</p>.+?<div class="star clearfix">.*?<span class="rating_nums">(.*?)</span>.*?<span class="pl">(.+?)</span>',
    re.DOTALL)

fb = Feedback()
for x in find_re.findall(html):
    iconUrl = x[0]  # icon
    link = x[1]  # 链接
    title = x[2]  # 片名 包含别名
    title = re.sub(patten2, '', title)
    content = x[3]  # 简介
    rating = x[4].strip()  # 评价
    rate_count = x[5]  # 评价数
    if rating:
        rateNum = str(int(float(rating)))
    else:
        rateNum = 'unknow'
        rating = '0.0'
    fb.add_item(rating+"\t"+title,
        subtitle=rate_count+"\t"+content,
        arg=link,icon='favicons/'+rateNum+'.png')
print fb