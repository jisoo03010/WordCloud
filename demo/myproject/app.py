#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re

import numpy as np  # 이미지 데이터를 다루기 위해
import pandas as pd  # 데이터를 다루기 위한 라이브러리
import time
from PIL import Image  # 이미지를 위한 라이브러리
from difflib import SequenceMatcher
from flask import Flask, render_template, request
import pymysql
from flask_sqlalchemy import SQLAlchemy
from wordcloud import WordCloud
import os
from collections import Counter
import matplotlib.pyplot as plt
from konlpy.tag import *
from nltk.stem import PorterStemmer, LancasterStemmer

#from sklearn.feature_extraction.text import CountVectorizer
db = SQLAlchemy()
app = Flask(__name__)

# rest api부분 =====================================

# /  : html template 보여줌
@app.route('/')
def index():
    #os.remove("./static/images/wordcloud_img.png")
    return render_template('index.html')



# 크롤링 데이터를 insert하는 db 부분 ============================
def insertDB(k, t, c1, c2, r):
    ret = []
    db = pymysql.connect(host='127.0.0.1', user='root',
                            port=3310,password='1234', charset='utf8', db='mydb')
    curs = db.cursor()
    sqlInsert = """
        insert into mydb.CrawlingNaverArticles(KeyWord, Title, ChangeContents, Contents, Registration_Date ) values( '{KeyWord1}' ,  '{Title1}', '{Contents1}', '{Contents2}',  '{Registration_Date1}' );
        """.format(KeyWord1=k, Title1=t, Contents1=c1, Contents2=c2, Registration_Date1=r )
    curs.execute(sqlInsert)
    db.commit()
    #db.close()
    return ret

# 워드 클라우드 부분 ============================

def word(text):
    
    wordcloud = WordCloud(font_path="./static/malgun.ttf",max_words=100, width = 800 , height = 400 ,background_color='white').generate(text)

    plt.figure()
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')
    os.remove('./static/images/wordcloud_img.png')
    
    plt.savefig('./static/images/wordcloud_img.png', bbox_inches='tight')

   

# 크롤링 데이터를 select db 부분 ============================



@app.route('/text',  methods=["POST"])
def selectDB():
    kyeword = request.get_json()        
    key = kyeword['keyword']
    print(key)
    ret = []
    db = pymysql.connect(host='master', user='root',
                            port=3306,password='1234', charset='utf8', db='mydb')
    curs = db.cursor()

   
    sqlInsert =  """ 
            SELECT ChangeContents
            FROM  mydb.crawlingnaverarticles
            WHERE Contents LIKE '%{keyword1}%';
            """.format(keyword1=key)
    

    curs.execute(sqlInsert)
  

    for i in curs:
        s = ''.join(map(str, i)).replace("\n", " ")
        ret.append(s)


    text = ''.join(list(set(ret)))
    
    last_arr = []
    arr = text.split(" ") 
    deleteArray  = ["통해", "기준", "계획", "당시", "앞서", "올해", "진행", "제공", "지난해", "지난달","다른","현재", "관련","모두","가장", "라며", "이번","또한","거나", "이후", "우리", "지금","연합뉴스", "예상", "로서", "대해" , "사진", "오늘", "최근", "지난", "위해", "때문", "대한"] 
    
    for i in arr:
        if i in deleteArray:
            continue
        else:
            s = ''.join(map(str, i))
            last_arr.append(s)
        
    text1 = ' '.join(last_arr)
    print(text1)
    """
    twt = Twitter()
    worss = twt.pos(text1)
    text_arr = []
    for i in worss:
        if  i[0] == "punctuation" and  i[0] == "Number" and i[0] == "Josa" and i[0] == "Foreign":
            continue
        elif i[0] == "@" or len(i[0]) > 1:
            text_arr.append(i[0])



    text2 = ''.join(text_arr).replace("\n", "")
    print(text2)
"""
    word(text1) 
    
    strings = text1.split()
    
    test_list2 = []
    social_news_word_count = Counter(strings)
    for i in social_news_word_count.most_common(51):
        test_list2.append(i)

        
    del test_list2[0]  

    db.commit()
    db.close()
    return test_list2

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9988)


"""
# 크롤링하는 부분 ============================
@app.route('/text',  methods=["POST"]) #  html 에서 받은 키워드 python으로 받기 위함
def crolling():
    kyeword = request.get_json()
    key = kyeword['keyword']
    dr = webdriver.Chrome(executable_path='C:/Windows/chromedriver.exe')
    for page_num in range(0, 10):
        # range를 이용하면 0부터 인덱스가 시작되므로 page_num에 1을 더해준 url을 이용
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={key}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=93&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={page_num}1'
        
        ActionChains(dr)  # 드라이버에 동작을 실행시키는 명령어를 act로 지정
        dr.get(url)
        html = dr.page_source
        soup = BeautifulSoup(html, 'html.parser')
        search_btn = dr.find_element(By.CLASS_NAME, 'bt_search')
        search_btn.click()
        
        links = soup.select('div.info_group > a.info')
      
        for link in links:
            # 포함되어 있으면  : 0 
            # 포함되어 있지 않으면 : -1 
            if link.get('href').find('https://n.news.naver.com/mnews/article') != -1: 
                dr.get(link['href'])
                time.sleep(2)
                if dr.current_url.find('https://n.news.naver.com/mnews/article')  != -1:
                    
                    kyeword = request.get_json()
                    key = kyeword['keyword'] # 키워드 
                    contents = dr.find_element(By.ID, 'dic_area') # 네이버 기사 컨텐츠 글
                    title = dr.find_element(By.ID, 'title_area') # 네이버 기사 제목 
                    date_time = dr.find_element(By.CLASS_NAME, '_ARTICLE_DATE_TIME') # 네이버 기사 입력 날짜  
               
                    contents_text = '\"'.join(contents.text.split("'"))
                    title_text = '\"'.join(title.text.split("'"))
                    date_time_text = '\"'.join(date_time.text.split("'"))
                    
  
                    print("================ title_text ===============\n")
                  
                    print(title_text)
                    print( "기사 입력 날짜 : " , date_time_text, "키워드 : " , key)
                    print("================ contents_text ===============\n")
                    print(contents_text)
                    # word(text) # word 클라우드 보여주는 함수에 파라미터 전달
                    
                    time.sleep(2)

                     #형태소 분석 
                
                    okt = Okt()
                    nouns = okt.nouns(contents_text) 


                    dd = ' '.join(v for v in nouns)
                    # print("======== 워드클라우드 시작 dd =======")
                    # print(dd)
                    list = dd.split(' ')
                            #print("======== 워드클라우드 시작 =======")
                    test_list = []
                    for item in list:
                        if  len(item) > 1:
                            test_list.append(item)
                    

                        
                    dd2 = ' '.join(v for v in test_list)
                    list2 = dd2.split(' ')

                    test_list2 = []
                    social_news_word_count = Counter(list2)
                    for i in social_news_word_count.most_common():
                        if i[0] == '기자':
                            continue
                        elif  i[0] == '오전':
                            continue
                        elif  i[0] == '때문':
                            continue
                        elif  i[0] == '오후':
                            continue
                        else :
                            test_list2.append(i[0])
                            #print(i)

                        
                    contents_text_change = ' '.join(v for v in test_list2)
                    list3 = contents_text_change.split(' ')



                    insertDB(key, title_text, contents_text_change, contents_text , date_time_text)
                    print("\n\n\n\n================================== 다음 글 ==================================")
                    dr.back()
                else :
                    dr.back()
                    
                #time.sleep(5)
        #print(page_num) 
          
    return kyeword


"""

