#!/usr/bin/python
#coding=utf-8

#添加测试数据

#导入sys,解决UnicodeEncodeError: 'ascii' codec can't encode characters in position 32-34: ordinal not in range(128)问题
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

import django
django.setup()

from django.contrib.auth.models import User
from app.models import UserProfile, Category, Article, Essays
import hashlib
import time

#添加user
def add_user(username, password, email, qq, icp, nickname, sex):
	password = hashlib.md5(password).hexdigest()
	u = User(username=username, password=password,email=email)
	u.save()
	up = UserProfile(user=u, sex=sex, nickname=nickname, qq=int(qq), icp=icp)
	up.save()
	return up

#添加文章分类
def add_category(user, name):
	cat = Category(user=user, name=name)
	cat.save()
	return cat

#添加文章
def add_article(user,category,title,author,content):
	article = Article(user=user, category=category, title=title,author=author, content=content)
	article.save()
	#分类中文章数量＋１
	category.count = category.count+1
	category.save()
	return article

#添加随笔　
def add_essays(user,title,author,content):
	essays = Essays(user=user,title=title,author=author,content=content)
	essays.save()
	return essays


#添加测试数据
def create_data():
	#添加user
	admin = add_user(username='admin', password='admin', email='admin@126.com', qq="1129946445", icp="张三", nickname="张三丰", sex='男')
	wang = add_user(username='wang', password='wang', email='wang@qq.com', qq="1235232232", icp="张五", nickname="张无忌", sex='男')
	zhao = add_user(username='zhao', password='zhao', email='zhao@163.com', qq="1723215194", icp="杨六", nickname="杨过", sex='女')

	#添加分类
	python = add_category(user=User.objects.get(id=admin.id), name='Python')
	php = add_category(user=User.objects.get(id=admin.id), name='PHP')
	add_category(user=User.objects.get(id=admin.id), name='HTML')
	add_category(user=User.objects.get(id=admin.id), name='CSS')
	add_category(user=User.objects.get(id=admin.id), name='Javascript')
	add_category(user=User.objects.get(id=admin.id), name='ajax')
	
	add_category(user=User.objects.get(id=wang.id), name='Linux/Unix')
	add_category(user=User.objects.get(id=wang.id), name='C/C++')
	add_category(user=User.objects.get(id=wang.id), name='IOS')
	
	add_category(user=User.objects.get(id=zhao.id), name='Oracle数据库')
	add_category(user=User.objects.get(id=zhao.id), name='Mysql数据库')

	#添加文章
	add_article(user=User.objects.get(id=admin.id), category=python, title="python基础学习", author=admin.nickname, content="学习python基础语法")
	time.sleep(1)
	add_article(user=User.objects.get(id=admin.id), category=python, title="django学习", author=admin.nickname, content="使用django开发移动web项目简介")
	time.sleep(1)
	add_article(user=User.objects.get(id=admin.id), category=python, title="django学习2", author=admin.nickname, content="Django是一个快速开发web的框架")
	time.sleep(1)

	add_article(user=User.objects.get(id=admin.id), category=php, title="php语言", author=admin.nickname, content="学习PHP的人说'php是世界上最好的语言'，然后学C的笑了！")

	#添加随笔
	content1="来传智播客学习快半年了，从一个一点不懂的小白开始学习，终于迎来了生命中的第一个软件项目，博客系统!"
	content2="这是测试随笔2,这是测试随笔2,这是测试随笔2,这是测试随笔2"
	content3="这是测试随笔3,这是测试随笔3,这是测试随笔3,这是测试随笔3,这是测试随笔3,"
	content4="这是测试随笔4,这是测试随笔4,这是测试随笔4,这是测试随笔4,这是测试随笔4,"
	content5="这是测试随笔5,这是测试随笔5,这是测试随笔5,这是测试随笔5,这是测试随笔5,"
	content6="这是测试随笔6,这是测试随笔6,这是测试随笔6,这是测试随笔6,这是测试随笔6,"
	content7="这是测试随笔7,这是测试随笔7,这是测试随笔7,这是测试随笔7,这是测试随笔7,"
	content8="这是测试随笔8,这是测试随笔8,这是测试随笔8,这是测试随笔8,这是测试随笔8,"
	add_essays(user=User.objects.get(id=admin.id), title="来传智播客学习", author=admin.nickname, content=content1)
	time.sleep(1)
	add_essays(user=User.objects.get(id=admin.id), title="随笔2", author=admin.nickname, content=content2)
	time.sleep(1)
	add_essays(user=User.objects.get(id=admin.id), title="随笔3", author=admin.nickname, content=content3)
	time.sleep(1)
	add_essays(user=User.objects.get(id=admin.id), title="随笔4", author=admin.nickname, content=content4)
	time.sleep(1)
	add_essays(user=User.objects.get(id=admin.id), title="随笔5", author=admin.nickname, content=content5)
	time.sleep(1)
	add_essays(user=User.objects.get(id=admin.id), title="随笔6", author=admin.nickname, content=content6)
	time.sleep(1)
	add_essays(user=User.objects.get(id=admin.id), title="随笔7", author=admin.nickname, content=content7)
	time.sleep(1)
	add_essays(user=User.objects.get(id=admin.id), title="随笔8", author=admin.nickname, content=content8)


	#打印添加的用户
	print '------添加的用户--------'
	for up in UserProfile.objects.all():
		print "{0}, {1}".format(str(up.user.username), str(up))
		
	#打印添加的分类
	print '------添加的分类--------'
	for cat in Category.objects.all():
		print "{0}, {1}".format(str(cat.user.username), str(cat.name))
		
	#打印添加文章
	print '------添加的文章--------'
	for at in Article.objects.all():
		print "{0}".format(str(at.title))
	
	#打印添加的随笔　
	print '------添加的随笔--------'
	for es in Essays.objects.all():
		print "{0}".format(str(es.title))


#执行代码
if __name__ == '__main__':
	print '开始构建测试数据...'
	create_data()
	print '数据构建完成!'


