#!/usr/bin/python
#-*-coding:utf-8 -*-

import requests,os,time,re
from bs4 import BeautifulSoup
import json
import random
import DAL



import sys
reload(sys)
sys.setdefaultencoding('utf8')

url = 'https://javmoo.com/cn/genre/28/page/'
#url = 'https://javmoo.com/cn/genre/1d/page/'
#url = 'https://javmoo.com/cn/search/JUY/page/'
def show_chinese(data):
    show_china = json.dumps(data, encoding='UTF-8', ensure_ascii=False)
    return show_china

def Out(s):
    f = open('/home/dyiwen/Desktop/av_id.log','a')
    f.write(s)
    f.close()


def get_page_url(url):
    urles = []
    for n in range(80,100):
        urls = url + '%s'%n
        urles.append(urls)
    print urles
    return urles


def get_url(url):
    headers = {
    'Connection': 'close',
    }
    req = requests.get(url,headers=headers)
    text = req.text
    #print text
    xx = 'https://javmoo.com/cn/movie/\w{3,6}'
    rex = re.compile(xx)
    result = rex.findall(text)
    print result
    print 'the total of find url :',len(result)
    return result

def search_word(url):
    headers = {
    'Connection': 'close',
    }
    req = requests.get(url,headers=headers)
    movie = []
    genre = []
    #print req.text
    xx = '<h3>(.*?)</h3>'
    rex_id = re.compile(xx)
    av_id = rex_id.search(req.text).group()
    print av_id[4:20]
    movie.append(av_id[4:20])
    #----------------------------------------------------------------------------------
    root_info = '<p><span class="genre">(.*?)</a></span></p>'
    print re.compile(root_info).search(req.text).group()
    #----------------------------------------------------------------------------------
    a = '<a href="https://javmoo.com/cn/genre(.*?)</a></span>'
    rex = re.compile(a)
    result = rex.findall(req.text)
    #print result
    for i in result:
        #print i
        xxx = '>(\S?){0,20}'
        rexx = re.compile(xxx)
        result2 = rexx.search(i).group()
        genre.append(result2)
    movie_ = '>'.join(genre[1:])
    movie.append(movie_)
    return movie

def go_get_word(url):
    urls = get_page_url(url)
    target_id = []
    for url in urls:
        movie_urls = get_url(url)
        print movie_urls
        for movie_url in movie_urls:
            n = 0
            aa =search_word(movie_url)
            aa.append(movie_url)
            #print aa
            a = show_chinese(aa)
            time.sleep(0.1)
            # if '连裤袜' in a or '恋腿癖' in a:
            if '女同性恋' in a :
                print a
                print aa,'------------------'
                insert_info_mysql(aa)
                target_id.append(a)
                Out(a+'\n')
            n += 1
            if n % 5 == 0:
                print 'witting a seconds'
                time.sleep(random.randint(1,2))
            if len(a) == 0:
                break


        time.sleep(0.5)
    print show_chinese(target_id)


def insert_info_mysql(info):
    msl = DAL.Mysql('127.0.0.1','3306','root','xnrdnh123','AV_info')
    sql = "insert id_info (av_id,genre,url_info) values ('{}','{}','{}');".format(info[0],info[1],info[2])
    print sql
    rowcount,result = msl.execute(sql)
    print result
    msl.close()

    return result
#------------------------------------------------------------------------------------
if __name__ == '__main__':
    #print movie
    # movie = search_word(url)
    # print show_chinese(movie)
    #get_url(url)
    #get_page_url(url)
    go_get_word(url)





'''<p><span class="genre">
<a href="https://javmoo.com/cn/genre/g">DMM独家
</a></span><span class="genre">
<a href="https://javmoo.com/cn/genre/1d">女同性恋
</a></span><span class="genre">
<a href="https://javmoo.com/cn/genre/1y">其他恋物癖
</a></span><span class="genre">
<a href="https://javmoo.com/cn/genre/2x">恋腿癖
</a></span><span class="genre">
<a href="https://javmoo.com/cn/genre/4a">女同接吻
</a></span><span class="genre">
<a href="https://javmoo.com/cn/genre/4o">高画质
</a></span></p>'''
