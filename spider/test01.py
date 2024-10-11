
import urllib.request
from urllib.request import Request
from uu import decode

from bs4 import BeautifulSoup
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='2011jz',
                             database='spider01_douban',
                             cursorclass=pymysql.cursors.DictCursor)


#创建一个Request(等于一个url),Request需要放在headers
h={
    "User-Agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36 (KHTML,like Gecko)Chrome/124.0.0.0 Safari/537.36"
}
req=urllib.request.Request("https://movie.douban.com/top250",headers=h)
r=urllib.request.urlopen(req)
print(r.status)
print(r.read().decode())



html_doc=r.read().decode()
#使用bs4或者re正则表达式来数据提取
soup=BeautifulSoup(html_doc,"html.parser")

items=soup.find_all("div",class_="item")#HTML的具体标签名

with connection:
   for item in items:
     img=item.find("div",class_="pic").a.img
     name=img["alt"]
     url=img["src"]

     #把提取的数据存储到mysql

     with connection.cursor() as cursor:
             # Create a new record
             sql = "INSERT INTO `movie_info` (`movie_name`, `movie_url`) VALUES (%s, %s)"
             cursor.execute(sql, (name,url))

         # connection is not autocommit by default. So you must commit to save
         # your changes.
   connection.commit()   #for循环全部循环结束再结束程序

'''
{
  "args": {},
  "headers": {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "httpbin.org",
    "Referer": "http://httpbin.org/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-66ece8eb-0cde07660af49843487fc64c"
  },
  "origin": "1.48.101.106",    #返回的ip
  "url": "http://httpbin.org/get"

}

'''




