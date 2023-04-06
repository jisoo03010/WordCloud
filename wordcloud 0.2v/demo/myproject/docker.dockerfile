
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




FROM python:3.10
# 필요한 패키지 설치
RUN apt-get update && \
    apt-get install -y python3-venv

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사
COPY . .

# 가상환경 생성 및 활성화
RUN python3 -m venv env
ENV PATH="/app/env/bin:$PATH"

# 필요한 라이브러리 설치
RUN pip install -r requirements.txt

# 컨테이너 실행 시 실행할 명령어 설정
CMD ["/bin/bash" , "-c" , "python app.py"] 