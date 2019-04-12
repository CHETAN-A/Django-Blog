from django.conf.urls import url, include
from django.contrib import admin
from .views import (
	CommentCreateAPIView, CommentDetailAPIView,
	CommentListAPIView )

urlpatterns = [
	url(r'^$', CommentListAPIView.as_view(),name="list" ),
	url(r'create/', CommentCreateAPIView.as_view(),name="create" ),
    # url(r'^(?P<idvalue>\d+)/delete/$', comment_delete, name="comment_delete" ),
    url(r'^(?P<id>\d+)/$', CommentDetailAPIView.as_view(),name="thread" ),
    # url(r'^(?P<id>\d+)/edit/$', CommentEditAPIView.as_view(),name="edit" ),
]