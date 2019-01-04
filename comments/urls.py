from django.conf.urls import url, include
from django.contrib import admin
from .views import comment_thread, comment_delete

urlpatterns = [
    url(r'^(?P<idvalue>\d+)/delete/$', comment_delete, name="comment_delete" ),
    url(r'^(?P<idvalue>\d+)/$', comment_thread,name="comment_thread" ),
]