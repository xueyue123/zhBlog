#!/bin/bash

#数据库操作准备工作
HOSTNAME="127.0.0.1"
USERNAME="root"
PASSWORD="123456"
DBNAME="blog"

#删除原来的数据库
drop_db_sql="drop database if exists ${DBNAME}"
mysql -h127.0.0.1 -P3306 -u${USERNAME} -p${PASSWORD} -e "${drop_db_sql}"

#重新创建数据库
create_db_sql="create database ${DBNAME} default character set utf8"
mysql -h127.0.0.1 -P3306 -u${USERNAME} -p${PASSWORD} -e "${create_db_sql}"

#删除旧快照文件
rm app/migrations/* -rf

#重新创建表
python manage.py migrate

#添加测试数据
python blog.py

#启动Django服务器
python manage.py runserver










