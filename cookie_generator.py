# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 21:58:44 2017

@author: fanweiming
"""

#%%
import urllib2  
import cookielib  
import requests  
from bs4 import BeautifulSoup  
import urllib  
import re  
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
loginUrl = 'http://accounts.douban.com/login'  
formData={  
    "redir":"http://movie.douban.com/mine?status=collect",  
    "form_email":'15650713602',  
    "form_password":'/15932200275/',  
    "login":u'登录'  
}  

cookie_filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(cookie_filename)
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
r = opener.open('https://movie.douban.com') 
cookie.save(ignore_discard=True, ignore_expires=True) 
 

#print r.url  