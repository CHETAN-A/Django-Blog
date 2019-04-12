from django.conf.urls import url, include
from django.contrib import admin
from posts.api.views import ( PostListAPIView, PostDetailAPIView,
							 PostUpdateAPIView, PostDeleteAPIView,
							 PostCreateAPIView )

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list' ),
    # url(r'^table/$', views.table, name='table' ),
    url(r'^create/$', PostCreateAPIView.as_view(),name="create" ),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name="delete" ),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view() , name="update"),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(),name="detail" ),
]