# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:08:58 2017

@author: fanweiming
"""

#%%
#文本分词，包括去除标点符号，停用词等等
import jieba
import re
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import defaultdict
from snownlp import SnowNLP
def remove_punctuation(sentence):
    sentence=sentence.decode('utf8')
    string_re=re.sub("[\s+\.\!\/_,$%^*(+\"\'a-zA-Z;]+|[+——！，。？、~@#￥%……&*（）0-9:：><]+".decode("utf8"), "".decode("utf8"),sentence)
    return string_re
def generator_stoplist(doc,n):
    f=open(doc,'r')
    frequency=defaultdict(int)
    for line in f.readlines():
        for word in list(jieba.cut(remove_punctuation(line))):
            frequency[word]+=1
    word_freq=sorted(frequency.iteritems(),key=lambda x:x[1],reverse=True)
    return [a for a,b in word_freq[:n]],word_freq  ####return a list
def get_doc_after_preprocessing(text,stop_list):
    f=open(text,'r')
    doc_collection=[]
    modify_doc=[]
    for line in f.readlines():
        doc_collection.append(' '.join(jieba.cut(remove_punctuation(line))))
    for doc in doc_collection:
        modify_doc.append(' '.join([word for word in doc.split(' ') if word not in stop_list]))
    return modify_doc    #return a list
def get_sentiment_label(doc):
    positive_score=[]
    assert (type(doc)==list),'doc is not list type'
    for line in doc:
        if not line=='':
            snow=SnowNLP(line.replace(' ',''))
            positive_score.append(snow.sentiments)
        else:
            positive_score.append(0.5)
    #assert len(positive_score)==len(doc),'length not equals between doc and label'
    return positive_score
'''
word_freq_tuple is a list in which each element is a tuple
for the tuple the first is a word,and the second is a int
'''
#picture_path is file path string
def get_wordCloud(word_freq_tuple,picture_path):
    from PIL import Image
    image=np.array(Image.open(picture_path))
    wc=WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',background_color = 'white', \
                 max_font_size = 50,min_font_size=10,random_state = 30,mask=image)
    wc.fit_words(dict(word_freq_tuple))
    return wc
def get_wordcloud_image(wc):
    import matplotlib.pyplot as plt
    plt.imshow(wc,interpolation='bilinear')
    plt.axis('off')
    plt.show()