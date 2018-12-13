# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.

class PostManager(models.Manager):
	def active(self,*args,**kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Post(models.Model):
	"""Model for Post"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1)
	title = models.CharField(max_length = 120)
	content = models.TextField()
	slug = models.SlugField(unique = True)
	draft = models.BooleanField(default= False)
	publish = models.DateField(auto_now= False,auto_now_add = False)
	image = models.ImageField(null = True, blank = True,height_field="height_field",width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

	objects = PostManager()
	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_abs_url(self):
		return reverse("posts:detail",kwargs = {"slug":self.slug})

	def get_abs_editurl(self):
		return reverse("posts:update",kwargs = {"slug":self.slug})

	def get_abs_deleteurl(self):
		return reverse("posts:delete",kwargs = {"slug":self.slug})
		# return "/posts/%s" %(self.id)

	class Meta:
		ordering = ["-timestamp","-updated"]

def create_slug(instance, new_slug= None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	# slug = slugify(instance.title)
	# exists = Post.objects.filter(slug=slug).exists()
	# if exists:
	# 	slug = "%s-%s" %(slugify(instance.title), instance.id)
	# instance.slug = slug
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)