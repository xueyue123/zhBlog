#coding=utf-8
from django.db import models
from datetime import  datetime
import hashlib
from django.template.defaultfilters import slugify	#slug
from django.contrib.auth.models import User

# Create your models here.
#-----------------------------------------------------------------------------------------------------------------------------------
#User模型
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	#使用User模型的username, password, email
	#自定义字段
	nickname = models.CharField(max_length = 32, default = "")
	qq = models.IntegerField(max_length = 20, default = "")
	sex = models.CharField(max_length = 5, blank = True)
	photo = models.ImageField('头像', upload_to='photos', blank = True, default = 'photos/default.png')
	icp = models.CharField(max_length = 128, default = "")
	time = models.DateTimeField(auto_now_add = True, default = datetime.now())
	def __unicode__(self):
		return self.sex
	class Meta:
		db_table = 'user'


#-----------------------------------------------------------------------------------------------------------------------------------
#分类模型
class Category(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 128, unique = True)
	count = models.IntegerField(default = 0)
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'category'

#为Category提供的表单模型，已弃用
class Temp(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	

#-----------------------------------------------------------------------------------------------------------------------------------
#文章模型
class Article(models.Model):
	user = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	title = models.CharField(max_length = 64, unique = True)
	author = models.CharField(max_length = 32, default = "")
	content = models.TextField()
	click = models.IntegerField(default = 0)
	tag = models.CharField(max_length = 64)
	date = models.DateField(auto_now_add = True, default = datetime.now())
	time = models.TimeField(auto_now_add = True, default = datetime.now())
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'article'
		ordering = ['-date', '-time']	#按时间由近及远排序

#-----------------------------------------------------------------------------------------------------------------------------------
#随笔模型
class Essays(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 64, unique = True)
	author = models.CharField(max_length = 32, default = "")
	content = models.TextField()
	click = models.IntegerField(default = 0)
	date = models.DateField(auto_now_add = True, default = datetime.now())
	time = models.TimeField(auto_now_add = True, default = datetime.now())
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'essays'
		ordering = ['-date', '-time']	#按时间由近及远排序

#评论模型
class Comment(models.Model):
	user = models.ForeignKey(User)
	article = models.ForeignKey(Article)
	#essays = models.ForeignKey(Essays)
	nickname = models.CharField(max_length = 32, default = "")
	content = models.CharField(max_length = 128)
	date = models.DateField(auto_now_add = True, default = datetime.now())
	time = models.TimeField(auto_now_add = True, default = datetime.now())
	def __unicode__(self):
		return self.content
	class Meta:
		db_table = 'comment'
		ordering = ['-date', '-time']	#按时间由近及远排序

#留言模型
class Message(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 64, default = "")
	author = models.CharField(max_length = 32, default = "")
	content = models.CharField(max_length = 200)
	date = models.DateField(auto_now_add = True, default = datetime.now())
	time = models.TimeField(auto_now_add = True, default = datetime.now())
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'message'
		ordering = ['-date', '-time']	#按时间由近及远排序

#相册模型
class Album(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 64, unique = True)
	path = models.ImageField('相片', upload_to='album', blank = True, default = 'photos/default.png')
	date = models.DateField(auto_now_add = True, default = datetime.now())
	time = models.TimeField(auto_now_add = True, default = datetime.now())
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'album'
		ordering = ['-date', '-time']	#按时间由近及远排序


#友情链接
class Link(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 64, unique = True)
	url = models.URLField()
	click = models.IntegerField(default = 0)
	date = models.DateField(auto_now_add = True, default = datetime.now())
	def __unicode__(self):
		return self.title
	class Meta:
		db_table = 'link'
		ordering = ['-date']	#按时间由近及远排序
