# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 09:50:34 2017

@author: fanweiming
"""
#%%
outfile='peopleName_comment.csv'
import pandas as pd
data=pd.read_csv('peopleName.csv',error_bad_lines=False)
data.columns=['name','support_num','comment']
print 'delete %d duplicate records' %(len(data)-len(data['comment'].unique()))
pd.DataFrame(data['comment'].unique()).to_csv(outfile,index=False,header=False,encoding='utf-8')
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
    string_re=re.sub("[\s+\.\!\/_,$%^*(+\"\'a-zA-Z;]+|[+——！，。？、~@#￥%……&*（）0-9:：><]+" \
    .decode("utf8"),"".decode("utf8"),sentence)
    return string_re
def generator_stoplist(text,n):
    f=open(text,'r')
    frequency=defaultdict(int)
    for line in f.readlines():
        for word in list(jieba.cut(remove_punctuation(line))):
            frequency[word]+=1
    word_freq=sorted(frequency.iteritems(),key=lambda x:x[1],reverse=True)
    return [a for a,b in word_freq[:n]],word_freq  ####return a list
def get_doc_after_preprocessing(text,stop_list):
    import pandas as pd
    f=open(text,'r')
    doc_collection=[]
    modify_doc=[]
    for line in f.readlines():
        doc_collection.append(' '.join(jieba.cut(remove_punctuation(line))))
    for doc in doc_collection:
        modify_doc.append(''.join([word for word in doc.split(' ') if word not in stop_list]))
    return pd.Series(modify_doc).unique().tolist()    #return a list
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
#modify_doc is list type
def split_doc_goodandbad(modify_doc,good_file_path,bad_file_path,label):
    fo1=open(good_file_path,'w')
    fo2=open(bad_file_path,'w')
    assert len(modify_doc)==len(label),"document list length not equals the length of label"
    for index,value in enumerate(label):
        if value>0.5:
            fo1.write(modify_doc[index].encode('utf-8'))
            fo1.write('\n')
        elif value<0.5:
            fo2.write(modify_doc[index].encode('utf-8'))
            fo2.write('\n')
    fo1.close()
    fo2.close()
    
def get_LDA_model(file_path,topic_num=3):
    import jieba.analyse
    from gensim import corpora, models  
    f1=open(file_path,'r')
    datalist=[]
    for i in f1.readlines():
        key_list=jieba.analyse.extract_tags(i.decode('utf-8'),30)
        datalist.append(key_list)  
    f1.close()
    dictionary=corpora.Dictionary(datalist)
    corpus = [dictionary.doc2bow(text) for text in datalist]
    #tfidf=models.TfidfModel(corpus)####统计tfidf
    #corpus_tfidf=tfidf[corpus]
    model = models.LdaModel(corpus, id2word=dictionary, \ 
            num_topics=topic_num,passes=20,iterations=500)
    return model
def get_stop_words(word_freq):
    for index,(a,b) in enumerate(word_freq[:20]):
        if type(a)=='unicode' and len(a)==1:
            del word_freq[index]
    return word_freq
            
            
        


#%%
'''
stoplist,word_freq_tuple=generator_stoplist(outfile,7)
wc=get_wordCloud(word_freq_tuple[10:],'none2.png')
get_wordcloud_image(wc)
########
plt.imshow(image,cmap=plt.cm.gray,interpolation='bilinear')
plt.axis("off")
plt.show()
#%%
from pprint import pprint
import jieba.analyse
from gensim import corpora, models  
f1=open('peopleName_comment.csv','r')
datalist=[]
for i in f1.readlines():
    key_list=jieba.analyse.extract_tags(i.decode('utf-8'),30)
    datalist.append(key_list)  
f1.close()
dictionary=corpora.Dictionary(datalist)
corpus = [dictionary.doc2bow(text) for text in datalist]
tfidf=models.TfidfModel(corpus)####统计tfidf
corpus_tfidf=tfidf[corpus]
model = models.LdaModel(corpus, id2word=dictionary, num_topics=NO,passes=20,iterations=500) 
#%%
#lsi=models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200) # initialize an LSI transformation
#corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
#lsi.print_topics(2)
NO=10
model = models.LdaModel(corpus, id2word=dictionary, num_topics=NO,passes=20,iterations=500) 
for i in range(NO):
    print '---------------------------'
    for a,b in model.show_topic(i):
        print a

'''
#%%
infile='peopleName.csv'
stop_list,word_freq=generator_stoplist(infile,10)
modify_doc=get_doc_after_preprocessing(infile,stop_list)
sentiment_label=get_sentiment_label(modify_doc)
good_file='good_comment.csv'
bad_file='bad_comment.csv'
split_doc_goodandbad(modify_doc,good_file,bad_file,sentiment_label)
#%%
_,good_word_freq=generator_stoplist(good_file,10)
_,bad_word_freq=generator_stoplist(bad_file,10)
good_word_freq=get_stop_words(good_word_freq)
bad_word_freq=get_stop_words(bad_word_freq)
wc_good=get_wordCloud(good_word_freq,'none2.png')
wc_bad=get_wordCloud(bad_word_freq,'none2.png')
get_wordcloud_image(wc_good)
get_wordcloud_image(wc_bad)
#%%

print int('777'
)























