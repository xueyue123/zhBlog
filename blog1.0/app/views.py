#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt		#去csrf保护
from django.contrib.auth.models import User
from json import loads, dumps
from django.core import serializers

from app.models import UserProfile, Category
from app.forms import UserForm, UserProfileForm, CategoryForm, TempForm
# Create your views here.

@csrf_exempt
def test(request):
	if request.method == 'POST' and request.is_ajax():
		content = request.POST.get('content')
		print content
		return HttpResponse(content)
	else:
		return render(request, 'admin/test.htm', {'name': 'get请求'})

@csrf_exempt
@login_required
def add(request):
	print 'post'
	if request.method == 'POST' and request.is_ajax():
		print 'aa'
		json_data = serializers.serialize("json", Category.objects.all())
		print json_data
		return HttpResponse(json_data,content_type="application/json")
	else:
		print 'ccc'
		return render(request, 'admin/test.htm', {})


