# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from .models import Comment
from .forms import CommentForm
# Create your views here.

@login_required
def comment_delete(request,idvalue):
	# obj = get_object_or_404(Comment,id=idvalue)
	try:
		obj = Comment.objects.get(id=idvalue)
	except:
		raise Http404
	if obj.user != request.user:
		# messages.success(request,"you do not have does not have permission.")
		# raise Http404
		response = HttpResponse('you do not have does not have permission.')
		response.status_code = 403
		return response

	if request.method == 'POST':
		parent_obj_url = obj.content_object.get_abs_url()
		obj.delete()
		messages.success(request,"This has been deleted.")
		return HttpResponseRedirect(parent_obj_url)
	context = {
	'object':obj
	}
	return render(request,'comment_delete.html',context)

def comment_thread(request,idvalue):
	# obj = get_object_or_404(Comment, id=idvalue)
	try:
		obj = Comment.objects.get(id=idvalue)
	except:
		raise Http404
	if not obj.is_parent:
		obj =obj.parent
	# print(obj.content)
	initial_data = {
	'content_type':obj.content_type,
	'object_id':obj.object_id
	}
	form = CommentForm(request.POST or None,initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		parent_obj = None
		try:
			print(form.cleaned_data)
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None
		print(parent_id)
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		new_comment, created = Comment.objects.get_or_create(
													user=request.user,
													content_type=content_type,
													object_id=obj_id,
													content=content_data,
													parent=parent_obj
												)
		if created:
			print("yeah it worked")
			print(created)
		return HttpResponseRedirect(new_comment.content_object.get_abs_url())
	context = {
	'comment':obj,
	'form': form
	}
	return render(request,'comment_thread.html',context)