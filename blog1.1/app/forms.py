#encoding:utf-8
from django import forms
from django.contrib.auth.models import User
from app.models import UserProfile, Category, Temp

#----------------------------------------------------------------------------------------------
#用户表单模型设计
class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'password', 'email')
		

#----------------------------------------------------------------------------------------------		
#用户表单模型设计
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('nickname', 'qq', 'sex', 'photo', 'icp')
	

#----------------------------------------------------------------------------------------------
#分类表单
class CategoryForm(forms.ModelForm):
	#user = User(username='wang', password = 'password'))
	#name = forms.CharField(max_length = 128, help_text = '分类名称')
	#user = forms.IntegerField(initial = 2)
	class Meta:
		model = Category
		fields = ('name', )

class TempForm(forms.ModelForm):
	class Meta:
		model = Temp
		fields = ('name', )



















