# WordCloud


![image](https://user-images.githubusercontent.com/73218962/225527052-467be0a3-4f7a-429c-a984-1fedf1aed94d.png)
                               
> ### 프로젝트 소개  
> __파이썬에서 제공하는 word cloud 모듈을 활용하여 개발을 진행하였다.   
> 모듈을 통해 word cloud를 개발함으로써 메타 데이터(네이버 기사 크롤링)에서 얻어진 태그들을 분석하여 중요도나 인기도 등을 고려하여 시각적으로 늘어놓아 표시하였다.
> 또한 단어의 크기는 많이 언급되는 순서대로 한눈에 들어올 수 있게 하였다.__  

## 
> __요구 사항__ 
>
> *  __docker image 다운로드__ 
>      * docker hub url : https://hub.docker.com/search?q=jisoo040310
>    * docker image 가져오는 명령어 
>        * mysql   
           <code> docker pull jisoo040310/mysql_last_image:latest</code>(:latest <- 생략가능)  
>        * web server  
           <code> docker pull jisoo040310/last_dockerweb_server:latest</code>(:latest <- 생략가능)
> * __docker 실행 명령어__ 
>   * __db server__ :  
     <code>docker run -it --rm --name [저장할 컨테이너의 이름] -e  MYSQL_ROOT_PASSWORD=1234 -p 3306:3306 [다운받은 mysql 이미지]  --character-set->server=utf8mb4 --collation-server=utf8mb4_unicode_ci </code>  
>   * __web server__ :    
      <code>docker run -it --rm  -p 0.0.0.0:8080:9988/tcp --name [저장할 컨테이너의 이름] --link [mysql server가 올라간 container 이름]:master [다운받은 flask web server]:[tag] </code>


## 
> __주요 기능__
> #### ⭐ 키워드 검색 기능 
> * 키워드의 제한이 없어 다양한 결과값을 보여줌 
> #### ⭐ 빈도수에 따른 키워드 순위표 & 이미지 시각화 가능  
> * 이미지를 보고 키워드의 순위가 예측이 되지 않는다면 표 테이블을 통해 확인가능



## 
> #### 배포 주소 : http://127.0.0.1:8080/

  















[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgjbae1212%2Fhit-counter&count_bg=%230C6CAA&title_bg=%23150A4F&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
