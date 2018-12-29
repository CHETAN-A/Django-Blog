# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Comment
# Create your views here.
def comment_thread(request,idvalue):
	obj = get_object_or_404(Comment, id=idvalue)
	return render(request,'comment_thread.html',{'obj':obj})