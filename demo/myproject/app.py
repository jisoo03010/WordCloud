from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import pymysql
from flask_sqlalchemy import SQLAlchemy
from konlpy.tag import Okt
import numpy as np  # 이미지 데이터를 다루기 위해
import pandas as pd  # 데이터를 다루기 위한 라이브러리
from wordcloud import WordCloud
from PIL import Image  # 이미지를 위한 라이브러리
import time
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
db = SQLAlchemy()
app = Flask(__name__)

# rest api부분 =====================================


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/text',  methods=["POST"])
def test():
   # data = request.get_json()
   # print(data)
    return "asdf"


class MyEmpDao:
    def getEmps(self):
        ret = []
        db = pymysql.connect(host='localhost', user='root',
                             port=3307, db='mydb', password='1234', charset='utf8')
        curs = db.cursor()

        sql = "select * from mydb.ServerDB"
        curs.execute(sql)

        rows = curs.fetchall()
        for e in rows:
            ret.append(e)
        db.commit()
        db.close()
        return ret


# 크롤링한 text data를 매개변수에 전달해서 =====================

def word(text):
    
    f = open("./static/dd.txt", "w", encoding='utf-8') # 파일 생성 
    print(text)
        # 크롤링한 데이터값 변수에 저장
    
    okt = Okt()
    nouns = okt.nouns(text) 

    # 명사만 추출
    for i in range(len(nouns)):
        f.write(nouns[i])


    dd = ' '.join(v for v in nouns)

    wordcloud = WordCloud(font_path="./static/malgun.ttf",max_words=20).generate(dd)
    
    plt.figure()
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()
# 크롤리 다 하고 디비에 넣고 디비에서 select핵서 화면에 뿌려주기
# 그럼 메모리 공간을 어떻게 해야하지?
# 디비에서 키워드에 맞는 문서 찾아다가 문서안에서 단어 쪼개서 wordcloud로 보여주기

#table마다 다르게 만들기 키워드 별로 만들면 될듯 그럼 ㅇㅋ

@app.route('/text',  methods=["POST"])
def crolling():
    kyeword = request.get_json()
    print(kyeword['keyword'])
    key = kyeword['keyword']

    dr = webdriver.Chrome(executable_path='C:/Windows/chromedriver.exe')
    for page_num in range(0, 1):
        print("dr ======")
        # time.sleep(3)
        # range를 이용하면 0부터 인덱스가 시작되므로 page_num에 1을 더해준 url을 이용
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={key}&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=93&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={page_num}1'
        print(dr)
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
                # 사이트 들어갔는데 url주소가 -> https://n.news.naver.com/mnews/article
                # 이게 들어가는 사이트이다? 그럼 contents 텍스트를 가져오고 
                # 아니라면 페이지를 전단계로 뒤로 돌린다.
                
                if dr.current_url.find('https://n.news.naver.com/mnews/article')  != -1:
                    contents = dr.find_element(By.ID, 'dic_area')
                    text =  contents.text
                    print(text)
                    
                    time.sleep(2)
                    print("\n===================================")
                    dr.back()
                else :
                    dr.back()
                    
                #
                #time.sleep(5)
        print(page_num) 
          
    return kyeword


"""
파일 내용 삭제 
    try:
    with open("./static/hitsong.txt", "w",'r+', encoding='utf-8') as f:
        f.truncate() # 파일 생성 
except IOError:
    print('Failure')

"""

if __name__ == '__main__':
   # emplist = MyEmpDao().getEmps()
   # print(emplist)
    app.run(debug=True, host='0.0.0.0', port=9090)



"""
def wordclouding(textdata):
    #굳이 파일로 변환안하고 형속변환만 해서 바로 돌려줘도 될듯 
    df = pd.read_csv('./static/test.txt', delimiter = '\t')
    text = ''.join(v for v in df['대한민국헌법'])
    okt = Okt()
    nouns = okt.morphs(text) # 명사만 추출
    dd = ' '.join(v for v in nouns)

    wordcloud = WordCloud( font_path = "./static/malgun.ttf",max_words=10).generate(dd)

    plt.figure()
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear') 
    plt.show()
    #cv2.imwrite('./static/images', img)
"""
