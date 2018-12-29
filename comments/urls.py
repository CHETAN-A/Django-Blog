from django.conf.urls import url, include
from django.contrib import admin
from .views import comment_thread

urlpatterns = [
    # url(r'^(?P<slug>[\w-]+)/delete/$', views.delete, name="delete" ),
    url(r'^(?P<idvalue>\d+)/$', comment_thread,name="comment_thread" ),
]