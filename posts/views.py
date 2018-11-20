# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

def create(request):
	if not request.user.is_superuser or not request.user.is_staff:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		print("begin")
		if form.is_valid():
			print("process")
			instance = form.save(commit=False)
			instance.save()
			messages.success(request,"Successfully Created")
			return HttpResponseRedirect(instance.get_abs_url())
		else:
			print("else")
			messages.error(request,"Not Successfully Created")
	# if request.method == "POST":
	# 	print request.POST.get("content")
	# 	print request.POST.get("title")
	context = {
	"form": form,
	}
	return render(request,"post_form.html",context)

def detail(request,slug):
	instance = get_object_or_404(Post, slug=slug)
	share_str = quote_plus(instance.content.encode('utf-8'))
	context = {
	"title" : instance.title,
	"obj": instance,
	"share_str": share_str,
	}
	return render(request,"post_detail.html",context)

def list(request):
	allobj_list = Post.objects.all() #.order_by("-timestamp")
	paginator = Paginator(allobj_list, 6) # Show 25 contacts per page

	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		allobj = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		allobj = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		allobj = paginator.page(paginator.num_pages)
	context = {
	"allobj":allobj,
	"title" : "Posts",
	"page" : page_request_var
	}
	# if request.user.is_authenticated():
	# 	context = {
	# 	"title" : "My List"
	# 	}
	# else:
	# 	context = {
	# 	"title" : "List"
	# 	}
	return render(request,"post_list.html",context)

def update(request,slug = None):
	if not request.user.is_superuser or not request.user.is_staff:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None , instance=instance)
	if request.method == "POST":
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request,"Successfully Saved")
			return HttpResponseRedirect(instance.get_abs_url())
		else:
			messages.error(request,"Failed Saving")
	context = {
	"title" : instance.title,
	"obj": instance,
	"form":form,
	}
	return render(request,"post_form.html",context)

def delete(request, slug=None):
	instance = get_object_or_404(Post,slug=slug)
	instance.delete()
	messages.success(request,"Item Deleted")
	return redirect("posts:list")
