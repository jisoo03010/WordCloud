FROM python:3.10.5-slim
RUN  apt-get update

COPY . /app
WORKDIR /app

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