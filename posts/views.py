# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

def create(request):
	if not request.user.is_superuser or not request.user.is_staff:
		raise Http404
	if not request.user.is_authenticated():
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		print("begin")
		if form.is_valid():
			print("process")
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			print(title)
			print(content)
			instance = form.save(commit=False)
			instance.user = request.user
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
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_superuser or not request.user.is_staff:
			raise Http404
	share_str = quote_plus(instance.content.encode('utf-8'))
	context = {
	"title" : instance.title,
	"obj": instance,
	"share_str": share_str,
	}
	return render(request,"post_detail.html",context)

def list(request):
	allobj_list = Post.objects.active() #.order_by("-timestamp")
	if request.user.is_superuser or request.user.is_staff:
		allobj_list = Post.objects.all()
	if request.method == "GET":
		query = request.GET.get("q")
		if query:
			allobj_list = allobj_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
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
	today = timezone.now().date()
	context = {
	"allobj":allobj,
	"title" : "Posts",
	"page" : page_request_var,
	"today" : today
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

def table(request):
	return render(request,'table.html')
