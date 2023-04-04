from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import io
import json
from sqlalchemy import create_engine
from PIL import Image
import base64
from io import BytesIO
import requests
import numpy as np  # 이미지 데이터를 다루기 위해
import pandas as pd  # 데이터를 다루기 위한 라이브러리
import time
from PIL import Image  # 이미지를 위한 라이브러리
from difflib import SequenceMatcher
from flask import Flask, render_template, request, jsonify
import pymysql
from flask_sqlalchemy import SQLAlchemy
from wordcloud import WordCloud
import os
from collections import Counter
import matplotlib.pyplot as plt
from konlpy.tag import *
from fake_useragent   import UserAgent
import ssl
from datetime import datetime, timedelta
import time
#from nltk.stem import PorterStemmer, LancasterStemmer
#from sklearn.feature_extraction.text import CountVectorizer
db = SQLAlchemy()
app = Flask(__name__)
# rest api부분 =====================================

# /  : html template 보여줌
@app.route('/')
def index():
    return render_template('index.html')

# 크롤링 데이터를 insert하는 db
def insertDB(k, t, c1, c2, r):
    ret = []
   #db = pymysql.connect(host='master', user='root',
    #                        port=3306,password='1234', charset='utf8', db='mydb')
    db = pymysql.connect(host='localhost', user='root',
                            port=3307,password='1234', charset='utf8', db='mydb')
    curs = db.cursor()
    sqlInsert = """
        REPLACE  into mydb.crawlingnaverarticles2( keyword, title, contents, change_contents, registration_date, now_time) values( '{keyword1}' ,  '{title1}','{contents1}', '{contents2}',  '{registration_date}',  date_format(now(), '%Y%m%d%H%i%s') );
        """.format(keyword1=k, title1=t, contents1=c1,  contents2=c2, registration_date=r )
    curs.execute(sqlInsert)
    db.commit()
    #print("insert 실행되었습니다!!1--------------")
    return ret

def chcingDataInsertDB(key , encode, textdata):
    ret = []
    db = pymysql.connect(host='localhost', user='root',
                            port=3307,password='1234', charset='utf8', db='mydb')
    curs = db.cursor()

    # 같은 키워드가 있을때 덮어쓰기해서 데이터 저장
    curs.execute("REPLACE into images(keyword, image_data, text_data) values( %s , %s ,  %s) ;", (key, encode, textdata))
    db.commit()
    print("chcingDataInsertDB insert 실행되었습니다!!1--------------")
    return ret
# 워드 클라우드 부분 ============================

def word(text):
    
    wordcloud = WordCloud(font_path="./static/malgun.ttf",max_words=100, width = 800 , height = 400 ,background_color='white').generate(text)
    
    print("================================ 성공적으로 wordcloud가 실행 되었습니다")
    file = "C:/Users/DataCentric/Desktop/WordCloud_Project/demo/myproject/static/images/wordcloud_img.png"
    if os.path.isfile("C:/Users/DataCentric/Desktop/WordCloud_Project/demo/myproject/static/images/wordcloud_img.png"):
        print("file이 있어요")
        os.remove(file)
    else :
        print("file이 없어요 ")
    
    plt.figure()
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')

    plt.savefig("C:/Users/DataCentric/Desktop/WordCloud_Project/demo/myproject/static/images/wordcloud_img.png", bbox_inches='tight')

# 크롤링 데이터를 select db 부분 ============================

def selectDB(key, sqlInsert, num ):
    print("key잘 받아왔습니다!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("keywrod : " , key)
    ret = []
    db = pymysql.connect(host='localhost', user='root',
                            port=3307,password='1234', charset='utf8', db='mydb')
    curs = db.cursor()
   
    
    print("sqlInsert : ", sqlInsert)
    print("num : ", num)

    curs.execute(sqlInsert)
    if num == 1 :

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
        strings = text1.split()
        
        test_list2 = []
        social_news_word_count = Counter(strings)
        for i in social_news_word_count.most_common(50):
            test_list2.append(i)
    

        textData_arr1 = []
        jsonData_arr2= []
        for i in test_list2:
            caching_data = {
                "keyword" : i[0],
                "count" : i[1]
            }
            jsonData_arr2.append(caching_data)
    
        json_data = json.dumps(jsonData_arr2, ensure_ascii=False)


        print(json_data)
        print(type(json_data))  
        textData = ' '.join(textData_arr1)
        print(textData)
        # 이미지 데이터 저장하는 부분
        # 이미지를 인코딩 한 값과 50위 안에 드는 키워드를 db에 저장
        with open('C:/Users/DataCentric/Desktop/WordCloud_Project/demo/myproject/static/images/wordcloud__after_img.png', mode='rb') as file:
            image = file.read()
            chcingDataInsertDB( key, image, json_data)
            
        db.commit()
        db.close()
        word(text1) 
        print("\n================================ 성공적으로 select메서드가 마무리 되었습니다")        
        

        return jsonify(json_data)
        
    else:
        print("10분 이내에 검색하고 키워드가 같으므로 기존에 있던 데이터를 그대로 가져옵니다.")
        ret2 = []
        for i in curs:
            # 바이너리 데이터를 이미지로 변환
            image = io.BytesIO(i[1])
            byteImg = Image.open(image)
            file_s = "C:/Users/DataCentric/Desktop/WordCloud_Project/demo/myproject/static/images/wordcloud_img.png"
            if os.path.isfile("C:/Users/DataCentric/Desktop/WordCloud_Project/demo/myproject/static/images/wordcloud_img.png"):
                os.remove(file_s)
            else :
                print("file이 없어요")
                byteImg.save('C:/Users/DataCentric/Desktop/WordCloud_Project/demo/myproject/static/images/wordcloud_img.png')
            # 이미지 파일로 저장
            ret2.append(i[0])
        print("\n\nret2===================")
        print(ret2)
        db.commit()
        db.close()
    

        return ret2
        


@app.route('/text',  methods=["POST"]) #  html 에서 받은 키워드 python으로 받기 위함
def crolling():    
    print("실행중,,,,, ")
    ssl._create_default_https_context = ssl._create_unverified_context
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    kyeword = request.get_json()
    print(kyeword)
    key = kyeword['keyword']
    before_key = kyeword['before_key']
    time = kyeword['timed']



    hour_t = datetime.today().hour        # 현재 시간 가져오기
    minute_t = datetime.today().minute      # 현재 분 가져오기
    second_t = datetime.today().second

    strr = str(hour_t) + ':' + str(minute_t) + ':' + str(second_t)

    now_time = datetime.strptime(strr, '%H:%M:%S')
    previous_time = datetime.strptime(time, '%H:%M:%S')
    print("\n\n==========================")
    print("now_time : ", now_time)
    print("previous_time  : ", previous_time)
    # 이전 시간과 현재 시간의 차이를 계산

    time_difference = now_time - previous_time
    print("현재 시간과 전 시간을 뺀값  : ",time_difference )



    for page_num in range(0, 10):
        url1 = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={key}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=93&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={page_num}1'
        response = requests.get(url1  , headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('div.info_group > a.info')

        for  i in links:
            if i.text == "네이버뉴스":
                url2 = i.attrs['href']
                response_contents = requests.get(url2, headers=headers)
                html2 = response_contents.text
                soup2 = BeautifulSoup(html2, 'html.parser')

                if response_contents.url.find('https://n.news.naver.com/mnews/article') != -1: 

                    title_text = soup2.select( '#title_area')[0].text.replace("\'","\"") # 네이버 기사 제목 
                    contents_text = soup2.select('div#dic_area')[0].text.replace("\'","\"") 
                    date_time_text = soup2.select( '._ARTICLE_DATE_TIME')[0].text.replace("\'","\"") # 네이버 기사 입력 날짜  

                    okt = Okt()
                    test_list = []
                    nouns = okt.nouns(contents_text) 
                    for item in nouns:
                        if  len(item) > 1:
                            test_list.append(item)

                    change_contents_text = ' '.join(v for v in test_list)


                    
                    # insertDB(key, title_text,contents_text,  change_contents_text, date_time_text)
                                # 차이가 1분 이내인지 판단하여 출력
                    if time_difference <= timedelta(minutes=2):
                        if   key == before_key:
                            print("키워드가 같고, 10분 이내에 검색하였습니다.")
                            sqlInsert1 =  """ 
                                            SELECT text_data , image_data 
                                            FROM  mydb.images
                                            WHERE keyword = '{keyword1}'
                                            group by  keyword;
                            """.format(keyword1=key)
                            num = 0
                        else :
                            # 새로운 뉴스가 나왔을수도 있으니 키워드에 대한 데이터를 업로드 시킴
                            # 하지만 db에 키워드가 있다면 ? update를 하는 것이고
                            # db에 키워드가 없다면 insert하는 것이다. 하지만 일단은 테스트이므로 insert 하도록 하겠다.
                            print("10분 이내에 검색하였지만 다른 키워드를 검색함")
                            sqlInsert1 =  """ 
                                        SELECT change_contents
                                        FROM  mydb.crawlingnaverarticles2
                                        WHERE contents LIKE '%{keyword1}%';
                                        """.format(keyword1=key)
                            num = 1
                            insertDB(key, title_text,contents_text,  change_contents_text, date_time_text)
                             
                    else:
                        print("10분 이내가 아닙니다.")
                        sqlInsert1 =  """ 
                                        SELECT change_contents
                                        FROM  mydb.crawlingnaverarticles2
                                        WHERE contents LIKE '%{keyword1}%';
                                        """.format(keyword1=key)
                        num = 1
                        insertDB(key, title_text,contents_text,  change_contents_text, date_time_text)

                    
                else :
                    continue
        
            
    return selectDB(key, sqlInsert1, num)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9988)


