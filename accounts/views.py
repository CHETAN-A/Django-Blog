# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout )
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
@csrf_protect
def login_view(request):
	next = request.GET.get('next')
	title = 'Login'
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username,password=password)
		login(request,user)
		if next:
			return redirect(next)
		return redirect('/')
		print(request.user.is_authenticated())
	return render(request,'form.html',{'form':form,'title':title})

@csrf_protect
def register_view(request):
	print(request.user.is_authenticated())
	title = 'Register'
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		login(request,user)
		return redirect('/')
	context = {
	'form':form,
	'title':title
	}
	return render(request,'form.html',context)

@csrf_protect
def logout_view(request):
	logout(request)
	return redirect('/')