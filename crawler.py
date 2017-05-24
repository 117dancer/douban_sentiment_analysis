# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 16:22:43 2017

@author: fanweiming
"""
#%%
import urllib2
from bs4 import BeautifulSoup
import bs4
lurl='https://movie.douban.com/top250'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
response=urllib2.urlopen(lurl)
soup=BeautifulSoup(response.read(),'html.parser')
print soup.prettify()
movie=[]
movielist=soup.select('.grid_view li')
#%%
def get_page(i):
    page_url='https://movie.douban.com/top250?start={}&filter='.format(i*25)
    return page_url
f=open('store_file','w')
for i in range(10):
    page_url=get_page(i)
    response=urllib2.urlopen(page_url)
    soup=BeautifulSoup(response.read(),'html.parser')
    movielist=soup.select('.grid_view li')
    for m in movielist:
        print '----------------------'
        rank = m.select('em')[0].text
        print 'rank:'+rank
        title = m.select('.title')[0].text
        print 'title:'+title
        movie_info= m.select('.info .bd p')[0].text.strip().split('\n')
    
        director=movie_info[0].strip().split(':')[1][:-2].rstrip()
        print 'director:'+director
        actor=movie_info[0].strip().split(':')[-1].strip()
        print 'actor:'+actor
        movie_type=movie_info[1].strip().split('/')[-1]
        print 'movie_type:'+movie_type
        produced_time=movie_info[1].strip().split('/')[0]
        print 'produced_time:'+produced_time
        country=movie_info[1].strip().split('/')[-2]
        print 'country:'+country
    

#movie.append('排名: '+ rank+ '\n' +'片名: '+ title + '\n'+ director + '\n' + '评论: '+ comments +'\n' + '\n')

#%% debug
single_movie=movielist[0]
def println(x):
    print x
print type(single_movie)
if type(single_movie)==bs4.element.Tag:
    print single_movie.select('em')[0].text
    print single_movie.select('.title')[0].text
    map(println,single_movie.select('.info .bd p')[0].text.strip().replace('\n','').split('/'))
    

    #print '\n主演:'.join(direct.split('   主演:'))
