# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:44:45 2017

@author: fanweiming
"""
#%%
ori_url='https://movie.douban.com/subject/26727273/comments?status=P'
bench_url='https://movie.douban.com/subject/26727273/comments'
import urllib2
from bs4 import BeautifulSoup
response=urllib2.urlopen(ori_url)
soup=BeautifulSoup(response.read(),'html.parser')
print soup.prettify()
#%%
#print soup.select('.comment-item')[0]
common_list=soup.select('.comment-item')
print len(common_list)
a=common_list[0]
print 'name:'+a.find('a')['title']
print 'link:'+a.find('a')['href']
print 'comment:'+a.find('p').text
print 'comment time:'+a.select('.comment-time')[0]['title']
print 'star num:'+a.select('.comment-time')[0] \
       .previous_sibling.previous_sibling['class'][0][-2:-1]
print 'support num:'+a.find('span',class_='votes').text

#%%
import cookielib
import urllib2
#创建MozillaCookieJar实例对象  
cookie = cookielib.MozillaCookieJar()  
#从文件中读取cookie内容到变量  
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)  
#利用urllib2的build_opener方法创建一个opener  
opener= urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  
my_userAgent=[
    "Mozilla/5.0 (Windows NT 5.1; rv:37.0) Gecko/20100101 Firefox/37.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"]
#%
def get_uerAgent(my_userAgent):
    import random
    length=len(my_userAgent)
    ran_index=random.choice(range(length))
    header={}
    header['User-Agent']=my_userAgent[ran_index]
    return header
#%
import random 
#import urllib2
from bs4 import BeautifulSoup
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
#Headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
url_parsered='https://movie.douban.com/subject/26727273/comments?status=P'
bench_url='https://movie.douban.com/subject/26727273/comments'
#f=open('douban_comment.txt','w')
page_count=0
print 'programe begins--------------------------'
while True:
    #url_parsered=ori_url
    #next_url=bench_url+next_page
    print 'this is one page------------------------'
    page_count+=1 
    time.sleep(random.choice(range(3,7)))
    print 'currnet page is------- '+str(page_count)
    Headers=get_uerAgent(my_userAgent)
    re=urllib2.Request(url_parsered,headers=Headers)
    re.add_header('referer','https://movie.douban.com/')
    response=opener.open(re)
    soup=BeautifulSoup(response.read(),'html.parser')
    common_list=soup.select('.comment-item')
    for element in common_list:
        name=element.find('a')['title']
        print '--------'+name
        link=element.find('a')['href']
        comment=element.find('p').text.strip().replace('\n','')
        #print name
        if len(element.select('.comment-time'))>0:
            comment_time=element.select('.comment-time')[0]['title']
            try:
                star_num=element.select('.comment-time')[0].previous_sibling.previous_sibling['class'][0][-2:-1]
            except KeyError:
                star_num=''
        else:
            comment_time=''
            star_num=''
        #star_num=element.select('.comment-time')[0].previous_sibling.previous_sibling['class'][0][-2:-1]
        support_num=element.find('span',class_='votes').text
        #f.write(name+'\t'+link+'\t'+comment+'\t'+comment_time+'\t'+star_num+'\t'+support_num)
        #f.write('\n')
    
    next_url=soup.find('a',class_='next')
    if not next_url:
        break
    url_parsered=bench_url+next_url['href']
#f.close()
#%%
count=0
while True:
    print 'shabiznemyang'+str(count)
    count+=1
    if count>10:
        break
#%%
import urllib2  
import cookielib  
#声明一个CookieJar对象实例来保存cookie  
cookie = cookielib.CookieJar()  
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器  
handler=urllib2.HTTPCookieProcessor(cookie)  
#通过handler来构建opener  
opener = urllib2.build_opener(handler)  
#此处的open方法同urllib2的urlopen方法，也可以传入request  
response = opener.open('https://movie.douban.com')  



#设置保存cookie的文件，同级目录下的cookie.txt  
filename = 'cookie.txt'  
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件  
cookie = cookielib.MozillaCookieJar(filename)  
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器  
handler = urllib2.HTTPCookieProcessor(cookie)  
#通过handler来构建opener  
opener = urllib2.build_opener(handler)  
#创建一个请求，原理同urllib2的urlopen  
response = opener.open("https://movie.douban.com")  
#保存cookie到文件  
cookie.save(ignore_discard=True, ignore_expires=True)   
#%%
#创建MozillaCookieJar实例对象  
cookie = cookielib.MozillaCookieJar()  
#从文件中读取cookie内容到变量  
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)  
#创建请求的request  
#req = urllib2.Request("https://movie.douban.com")  
#利用urllib2的build_opener方法创建一个opener  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  
response = opener.open(req)  
print response.read()  



