#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt		#去csrf保护
from django.contrib.auth.models import User
from json import loads, dumps
from django.core import serializers

from app.models import UserProfile, Category, Article
from app.forms import UserForm, UserProfileForm, CategoryForm, TempForm

#---------------views function---------------
def index(request):
	return HttpResponse("无内容")

