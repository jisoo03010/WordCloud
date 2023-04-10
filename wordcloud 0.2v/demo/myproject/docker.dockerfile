
#FROM mysql:8.0
#ENV LC_ALL=C.UTF-8
#ENV character-set-server utf8
#ENV collation-server utf8_general_ci
#ENV default-character-set utf8
#ENV default-collation utf8_general_ci
#
#ENV MYSQL_ROOT_PASSWORD=1234
#ENV MYSQL_PASSWORD=1234
#ENV MYSQL_DATABASE="mydb"
#
#COPY  mydb_images.sql /docker-entrypoint-initdb.d 
#COPY  mydb_crawlingnaverarticles2.sql /docker-entrypoint-initdb.d 


FROM python:3.10.5-slim
RUN  apt-get update

COPY . /app
WORKDIR /app


RUN apt-get install -y default-jdk default-jre
RUN pip3 install requests
RUN pip3 install fake_useragent
RUN pip3 install bs4
RUN pip3 install flask
RUN pip3 install wordcloud
RUN pip3 install selenium  
RUN pip3 install konlpy  
RUN pip3 install numpy  
RUN pip3 install pandas  
RUN pip3 install pymysql  
RUN pip3 install flask_sqlalchemy  
RUN pip3 install matplotlib  
RUN pip3 install nltk 
RUN pip3 install cryptography 

ENTRYPOINT python app.py