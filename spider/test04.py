
import urllib.request
from urllib.request import Request
from uu import decode

from bs4 import BeautifulSoup
import pymysql.cursors
from lxml import etree

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='2011jz',
                             database='spider01_douban',
                             cursorclass=pymysql.cursors.DictCursor)

#发起网络请求
url="https://movie.douban.com/top250"

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

#获取标题
def get_first_text(list):
    try:
      return list[0].strip()   #标题返回是一个列表形式，所以使用一个函数来解决,strip除去空格
    except:
        return ""    #有些电影没有简介，返回空值

#https://movie.douban.com/top250?start=0&filter=   第一页
#https://movie.douban.com/top250?start=25&filter=  第二页
#https://movie.douban.com/top250?start=50&filter=   第三页
#得到十个页面的url地址
urls=['https://movie.douban.com/top250?start={}&filter='.format(str(i*25)) for i in range(10)]
count=1   #计数
for url in urls:

    res =urllib.request.Request(url=url,headers=headers) #发出请求


    # 1整个列表标签
    html = etree.HTML(res.text)  #将返回的文本加工为可以解析的html
    lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')  #获取每个电影的li元素

    print(len(lis))#打li标签长度
# 解析数据
for li in lis :
    title=get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))
    src=get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))  #在标题后打印链接
    dictor=get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()')) #获取导演信息
    score=get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))#获取评分
    comment=get_first_text(li.xpath('.div/div[2]/div[2]/div/span[4]/text()'))#评价
    summary=get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))#简介

    print(count,title,src,dictor,score,comment,summary)
    count +=1




