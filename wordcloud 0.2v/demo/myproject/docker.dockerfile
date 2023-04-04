FROM mysql:8.0

ENV LC_ALL=C.UTF-8
ENV character-set-server utf8
ENV collation-server utf8_general_ci
ENV default-character-set utf8
ENV default-collation utf8_general_ci

ENV MYSQL_ROOT_PASSWORD=1234
ENV MYSQL_PASSWORD=1234
ENV MYSQL_DATABASE="mydb"

COPY  word_cloud_sql_dump_file.sql /docker-entrypoint-initdb.d 