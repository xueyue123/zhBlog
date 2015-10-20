#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt		#去csrf保护
from django.contrib.auth.models import User
from json import loads, dumps
from django.core import serializers

from app.models import UserProfile, Category, Article, Essays, Comment, Message,Album, Link
from app.forms import UserForm, UserProfileForm, CategoryForm, TempForm
# Create your views here.

#=========================================================================================================
#博客后台

#后台管理
@login_required
def admin(request):
	user = request.user
	return render(request, 'admin/admin.htm', {'user': user})

#用户退出
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

#用户信息的入口，头像，密码等
@login_required
def change_password(request):
	return HttpResponseRedirect('/change_password/')


#分类管理
@login_required
def category_manage(request):
	category_list = Category.objects.filter(user = request.user)
	content_dict = {'categories': category_list}
	return render(request, 'admin/category_manage.htm', content_dict)

#添加分类
@csrf_exempt
@login_required
def add_category(request):
	if request.method == 'POST' and request.is_ajax():
		category_name = request.POST.get('name')
		if category_name == '':
			return HttpResponse("分类名称不能为空")
		#print category_name		#打印分类名称
		user = User.objects.get(username = request.user.username)
		#print user.username		#打印当前用户名
		category = Category(name=category_name, user=user)
		category.save()
		return HttpResponse("添加成功")	#ajax post要返回一个值,否则报500错误
	else:
		#print 'get请求, 返回管理界面！'
		category_list = Category.objects.filter(user = request.user)
		#category_list = Category.objects.all()
		content_dict = {'categories': category_list}
		return render(request, 'admin/category_manage.htm', content_dict)
		#return render(request, 'admin/category_manage.htm', {})

#删除分类
@csrf_exempt
@login_required
def del_category(request):
	if request.method == 'POST' and request.is_ajax():
		cid = request.POST.get('id')	#cid ->category id
		print cid
		category = Category.objects.get(id=cid)
		category.delete()
		category_list = Category.objects.filter(user = request.user)
		content_dict = {'categories': category_list}
		return render(request, 'admin/category_manage.htm', content_dict)
	else:
		category_list = Category.objects.filter(user = request.user)
		content_dict = {'categories': category_list}
		return render(request, 'admin/category_manage.htm', content_dict)

#文章管理
@login_required
def article_manage(request):
	user = User.objects.get(username = request.user.username)
	category_list = Category.objects.filter(user=user)
	#print user.username
	article_list = Article.objects.filter(user = user)
	article_dict = {'articles': article_list, 'categories': category_list}
	return render(request, 'admin/article_manage.htm', article_dict)

#添加文章
@csrf_exempt
@login_required
def add_article(request):
	if request.method == 'POST' and request.is_ajax():
		#获取post提交的数据
		category_name = request.POST.get('category')
		title = request.POST.get('title')
		author = request.POST.get('author')
		content = request.POST.get('content')
		#print 'category:' + category_name + ' title:' + title + '  author:' + author + '  content:' + content 	#打印POST请求的内容
		
		#创建Article对象，保存文章
		user = User.objects.get(username = request.user.username)
		category = Category.objects.get(name = category_name)
		add = request.POST.get('add')
		if add == 'false':		#编辑文章
			pass
		else:
			print request.POST.get('id')
			category.count = category.count + 1
			category.save()
		article = Article(user=user, category=category, title=title, content=content, author=author)
		article.id = request.POST.get('id')	#如果是编辑文章将会获取到原文章的id, 如果是添加文章则获取到none
		article.save()
		category_list = Category.objects.filter(user = request.user)
		content_dict = {'categories': category_list}
		return HttpResponse("添加成功")
	else:
		category_list = Category.objects.filter(user = request.user)
		userprofile = UserProfile.objects.get(id = request.user.id)
		content_dict = {'categories': category_list, 'userprofile': userprofile}
		return render(request, 'admin/add_article.htm', content_dict)

#编辑文章
@csrf_exempt
@login_required
def edit_article(request):
	if request.method == 'POST' and request.is_ajax():
		return render(request, 'admin/edit_article.htm', {})
	else:
		aid = request.GET['id']		#aid ->article id
		aid = int(aid)
		article = Article.objects.get(id=aid)
		category_list = Category.objects.filter(user = request.user)
		content_dict = {'article': article, 'categories': category_list}
		return render(request, 'admin/edit_article.htm', content_dict)
	
#删除文章
@csrf_exempt
@login_required
def del_article(request):
	if request.method == 'POST' and request.is_ajax():
		aid = request.POST.get('id')	#aid ->article id
		article = Article.objects.get(id=aid)
		#删除文章时分类中的文章数-1
		category = Category.objects.get(id=article.category.id)
		category.count = category.count -1
		category.save()
		#删除文章
		article.delete()
		article_list = Article.objects.filter(user = request.user)
		content_dict = {'articles': article_list}
		return render(request, 'admin/article_manage.htm', content_dict)
	else:
		article_list = Article.objects.filter(user = request.user)
		content_dict = {'articles': article_list}
		return render(request, 'admin/article_manage.htm', content_dict)


#随笔管理
@login_required
def essays_manage(request):
	essays_list = Essays.objects.filter(user = request.user.id)
	content_dict = {'essays': essays_list}
	return render(request, 'admin/essays_manage.htm', content_dict)

#添加随笔
@csrf_exempt
@login_required
def add_essays(request):
	if request.method == 'POST' and request.is_ajax():
		#获取post提交的数据
		eid = ''
		title = request.POST.get('title')
		author = request.POST.get('author')
		content = request.POST.get('content')
		#print 'category:' + category_name + ' title:' + title + '  author:' + author + '  content:' + content 	#打印POST请求的内容
		
		#创建Article对象，保存文章
		user = User.objects.get(username = request.user.username)
		add = request.POST.get('add')
		if add == 'false':		#编辑文章
			eid = request.POST.get('id')
			essays = Essays.objects.get(id=eid)
			essays.delete()
			print 'delete essays success'
		else:
			pass
		essays = Essays(user=user, title=title, content=content, author=author)
		if eid != '':
			essays.id = eid
		essays.save()
		return HttpResponse("添加成功")
	else:
		userprofile = UserProfile.objects.get(id = request.user.id)
		content_dict = {'userprofile': userprofile}
		return render(request, 'admin/add_essays.htm', content_dict)

#编辑随笔
@csrf_exempt
@login_required
def edit_essays(request):
	if request.method == 'POST' and request.is_ajax():
		return render(request, 'admin/edit_essays.htm', {})	#这句话没有机会执行，因为edit_essays.htm提交后会交给add_essays处理
	else:
		eid = request.GET['id']		#eid ->essays id
		print eid
		essays = Essays.objects.get(id=eid)
		content_dict = {'essays': essays}
		return render(request, 'admin/edit_essays.htm', content_dict)

#删除随笔
@csrf_exempt
@login_required
def del_essays(request):
	if request.method == 'POST' and request.is_ajax():
		eid = request.POST.get('id')	#cid ->category id
		essays = Essays.objects.get(id=eid)
		essays.delete()
		essays_list = Essays.objects.filter(user = request.user)
		content_dict = {'essays': essays_list}
		return render(request, 'admin/essays_manage.htm', content_dict)
	else:
		essays_list = Essays.objects.filter(user = request.user)
		content_dict = {'essays': essays_list}
		return render(request, 'admin/essays_manage.htm', content_dict)

#评论管理
@login_required
def comment_manage(request):
	comment_list = Comment.objects.filter(user = request.user)
	content_dict = {'comments': comment_list}
	return render(request, 'admin/comment_manage.htm', content_dict)

#查找评论
@login_required
def find_comment(request):
	return HttpResponse("暂无内容")

#删除评论
@csrf_exempt
@login_required
def del_comment(request):
	if request.method == 'POST' and request.is_ajax():
		cid = request.POST.get('id')
		comment = Comment.objects.get(id = cid)
		comment.delete()
		return HttpResponse("删除成功")
	else:
		pass


#留言管理
@login_required
def message_manage(request):
	message_list = Message.objects.filter(user = request.user)
	content_dict = {'messages': message_list}
	return render(request, 'admin/message_manage.htm', content_dict)

#查找留言
@login_required
def find_message(request):
	return HttpResponse("暂无内容")


#删除评论
@csrf_exempt
@login_required
def del_message(request):
	if request.method == 'POST' and request.is_ajax():
		cid = request.POST.get('id')
		message = Message.objects.get(id = cid)
		message.delete()
		return HttpResponse("删除成功")
	else:
		pass


#相册管理
@login_required
def album_manage(request):
	album_list = Album.objects.filter(user = request.user)
	content_dict = {'albums': album_list}
	return render(request, 'admin/album_manage.htm', content_dict)

@login_required
def add_album(request):
	return HttpResponse("暂无内容")

#友情链接管理
@login_required
def link_manage(request):
	link_list = Link.objects.filter(user = request.user)
	content_dict = {'links': link_list}
	return render(request, 'admin/link_manage.htm', content_dict)


@login_required
def add_link(request):
	return HttpResponse("暂无内容")

def advertisement_manage(request):
	return HttpResponse('暂无内容')

@login_required
def user_setting(request):
	user = User.objects.get(id = request.user.id)
	userprofile = UserProfile.objects.get(user = user)	
	if request.method == 'POST':
		password = request.POST.get('password')
		if password == '':
			return HttpResponse('密码不能为空<h2><a href="#" onclick="history.go(-1)""> 返回 </a></h2>')
		email = request.POST.get('email')
		nickname = request.POST.get('nickname')
		qq = request.POST.get('qq')
		icp = request.POST.get('icp')
		#保存密码和邮箱
		user.set_password(password)
		user.email = email
		user.save()
		#保存其它信息
		userprofile.nickname = nickname
		userprofile.qq = qq
		userprofile.icp = icp
		userprofile.save()
		return HttpResponse('更新数据成功<h2><a href="/admin/"> 返回 </a></h2>')
	else:
		content_dict = {'user': user, 'userprofile': userprofile}
		return render(request, 'admin/user_setting.htm', content_dict)


def data_backup(request):
	return HttpResponse('暂无内容')
def data_restore(request):
	return HttpResponse('暂无内容')
def clean_cache(request):
	return HttpResponse('暂无内容')
