#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt		#去csrf保护
from django.contrib.auth.models import User
from json import loads, dumps
import json
from django.core import serializers

from app.models import UserProfile, Category, Article, Essays, Comment, Message, Album, Link
from app.forms import UserForm, UserProfileForm, CategoryForm, TempForm
# Create your views here.

#=========================================================================================================
#博客前台

#用户注册
def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit = False)
			profile.user = user

			if 'photo' in request.FILES:
				profile.photo = request.FILES['photo']

			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
	return render(request, 'blog/register.htm', dict)

#用户登录
def user_login(request):
	#print 'user_login()被调用了'
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		#print 'username=', username, 'password=', password
		#验证用户名和密码
		user = authenticate(username = username, password = password)
		if user:
			#print 'username:', user.username
			if user.is_authenticated():
				#print '登录成功'
				login(request, user)
				return HttpResponseRedirect('/admin/')
		else:
			print '用户名或密码错误'
			return render(request, 'admin/login.htm', {'error': '用户名或密码错误'})
	else:
		print 'get请求, 返回登录表单给用户'
		return render(request, 'admin/login.htm', {})


#博客首页
def index(request):
	user = User.objects.get(id=1)
	userprofile = UserProfile.objects.get(id = user.id)
	category_list = Category.objects.filter(user=user)
	essays_list = Essays.objects.filter(user=user.id)[:8]
	pages = request.GET.get('page')
	#print pages
	if pages == 'category_article_list':	#显示分类下的文章列表
		category = Category.objects.get(id=request.GET['id'])
		article_list = Article.objects.filter(category=category)
		content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'category': category, 'page': pages}
	elif pages == 'article_list':		#显示所有文章列表
		#article_list = Article.objects.order_by("date", "time")
		article_list = Article.objects.filter(user=user)[:8]		#取最近的5篇文章显示在首页,在模型中已经对文章进行排序
		#article_list
		content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'page': pages}
	elif pages == 'read_article':		#显示文章内容
		aid = int(request.GET['id'])
		article = Article.objects.get(id = aid)
		comment_list = Comment.objects.filter(article = article)
		content_dict = {'article': article, 'categories': category_list, 'essays': essays_list, 'comments': comment_list, 'page': pages}
	elif pages == 'all_essays_list':		#显示所有随笔列表
		all_essays_list = Essays.objects.filter(user=user)
		content_dict = {'allessays': all_essays_list, 'categories': category_list, 'essays': essays_list, 'page': pages}
	elif pages == 'read_essays':		#显示随笔内容
		essay = Essays.objects.get(id = request.GET['id'])
		content_dict = {'categories': category_list, 'essays': essays_list, 'essay': essay, 'page': pages}
	elif pages == 'commit_comment':
		aid = int(request.GET['id'])
		article = Article.objects.get(id = aid)
		nickname = request.GET.get('nickname')
		content = request.GET.get('content')
		if nickname == '':
			return HttpResponse("1")
		elif content == '':
			return HttpResponse("2")
		comment = Comment(user = user, article = article, nickname = nickname, content =content)
		comment.save()
		#print nickname + content
		comment_list = Comment.objects.filter(article = article)
		content_dict = {'article': article, 'categories': category_list, 'essays': essays_list, 'comments': comment_list, 'page': 'read_article'}
		return HttpResponse("评论成功")
	elif pages == 'message':
		article_list = Article.objects.filter(user=user)
		content_dict = {'categories': category_list, 'essays': essays_list, 'page': pages}
	else:					#其它
		article_list = Article.objects.filter(user = user)[:8]
		content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'page': 'index_page', 'user': user, 'userprofile': userprofile}
		#print content_dict
	return render(request, 'blog/index.htm', content_dict)


def essays(request):
	return HttpResponse('暂无内容')
	
def album(request):
	return HttpResponse('暂无内容')
	
@csrf_exempt
def message(request):
	user = User.objects.get(id=1)
	if request.method == 'POST':
		nickname = request.POST.get('nickname')
		title = request.POST.get('title')
		content = request.POST.get('content')
		if nickname == '':
			return HttpResponse('感谢您的支持! 但昵称不可为空哦！<h2><a href="/">返回主页</a></h2>')
		elif title == '':
			return HttpResponse('感谢您的支持! 但标题不可为空哦！<h2><a href="/">返回主页</a></h2>')
		elif content == '':
			return HttpResponse('感谢您的支持! 但内容不可为空哦！<h2><a href="/">返回主页</a></h2>')		
		#print nickname
		message = Message(user=user, author=nickname, title=title, content=content)
		message.save()
		return HttpResponse('留言成功，感谢您的支持! <h2><a href="/">返回主页</a></h2>')
	else:
		return HttpResponse('留言失败感谢您的支持! <h2><a href="/">返回主页</a></h2>')
	
def author(request):
	return HttpResponse('暂无内容')
	
def subscribe(request):
	return HttpResponse('暂无内容')
	
def collect(request):
	return HttpResponse('暂无内容')

'''
#装饰器函数
def mylogin_required(func):
	def _deco(request):
		#print '装饰器被调用了！'
		#user_login(request)
		#func(request)
		return render(request, 'admin/login.htm')
	return _deco
'''

'''
#博客首页
def index(request):
	user = User.objects.get(id=1)
	userprofile = UserProfile.objects.get(id=user.id)
	category_list = Category.objects.filter(user=user)
	article_list = Article.objects.filter(user=user)
	essays_list = Essays.objects.filter(user=user)[:10]
	content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'page': 'index_page', 'user': user, 'userprofile': userprofile}
	return render(request, 'blog/index.htm', content_dict)
'''

'''
#博客主页相关访问链接
def index2(request):
	user = User.objects.get(id=1)
	userprofile = UserProfile.objects.get(id = user.id)
	category_list = Category.objects.filter(user=user)
	essays_list = Essays.objects.filter(user=user.id)[:8]
	pages = 'index_page'
	pages = request.GET.get('page')
	print pages
	if pages == 'category_article_list':	#显示分类下的文章列表　
		category = Category.objects.get(id=request.GET['id'])
		article_list = Article.objects.filter(category=category)
		content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'category': category, 'page': pages}
	elif pages == 'article_list':		#显示所有文章列表
		article_list = Article.objects.filter(user=user)
		content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'page': pages}
	elif pages == 'read_article':		#显示文章内容
		aid = int(request.GET['id'])
		article = Article.objects.get(id = aid)
		content_dict = {'article': article, 'categories': category_list, 'essays': essays_list, 'page': pages}		
	elif pages == 'all_essays_list':		#显示所有随笔列表
		all_essays_list = Essays.objects.filter(user=user)
		content_dict = {'allessays': all_essays_list, 'categories': category_list, 'essays': essays_list, 'page': pages}
	elif pages == 'read_essays':		#显示随笔内容
		essay = Essays.objects.get(id = request.GET['id'])
		content_dict = {'categories': category_list, 'essays': essays_list, 'essay': essay, 'page': pages}
	else:					#其它
		article_list = Article.objects.filter(user=user)
		content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'page': 'index_page', 'user': user, 'userprofile': userprofile}
	return render(request, 'blog/index.htm', content_dict)
'''

'''
#显示所有文章
def article(request):
	user = User.objects.get(id=1)
	article_list = Article.objects.all()
	category_list = Category.objects.filter(user = user.id)
	article_list = Article.objects.all()
	essays_list = Essays.objects.filter(user=user)
	content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'page': 'article_list'}
	return render(request, 'blog/index.htm', content_dict)
'''
'''
#显示文章内容
def defarticle(request, article_id):
	user = User.objects.get(id=1)
	article = Article.objects.get(id=int(article_id))
	article.click = article.click + 1
	article.save()
	category_list = Category.objects.filter(user = user.id)
	article_list = Article.objects.all()
	essays_list = Essays.objects.filter(user=user)
	content_dict = {'article': article, 'categories': category_list, 'essays': essays_list, 'page': 'article_page'}
	return render(request, 'blog/index.htm', content_dict)
'''
'''
#显示指定分类的文章　
def category_article(request):
	print request.GET['page']
	user = User.objects.get(id=1)
	category_id = request.GET['id']
	category = Category.objects.get(id=category_id)
	article_list = Article.objects.filter(category=category)
	category_list = Category.objects.filter(user = user.id)
	essays_list = Essays.objects.filter(user=user)
	content_dict = {'articles': article_list, 'categories': category_list, 'essays': essays_list, 'category': category, 'page': 'category_article_page'}
	#print category.id
	return render(request, 'blog/index.htm', content_dict)
'''