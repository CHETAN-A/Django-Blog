from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from posts.models import Post
from comments.api.serializers import CommentSerializer
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
		# 'id',
		'title', 
		# 'slug' ,
		'content',
		'publish',
		]

post_detail_url = HyperlinkedIdentityField(view_name='posts_api:detail',lookup_field='slug')

class PostDetailSerializer(ModelSerializer):
	url = post_detail_url
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()

	class Meta:
		model = Post
		fields = ['url','id','title', 'slug' ,'content','publish','user','image','html','comments']

	def get_user(self,obj):
		return str(obj.user.username)

	def get_image(self,obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

	def get_html(self,obj):
		return obj.get_markdown()

	def get_comments(self,obj):
		content_type = obj.get_content_type
		obj_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentSerializer(c_qs,many=True).data
		return comments

class PostListSerializer(ModelSerializer):
	url = post_detail_url
	# delete_url = HyperlinkedIdentityField(view_name='posts_api:delete',lookup_field='slug')
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()

	class Meta:
		model = Post
		fields = ['url','id','title', 'slug' ,'content','image','publish','user']

	# def get_user(self,obj):
	# 	return str(obj.user.username)

	def get_image(self,obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

"""
from posts.models import Post
from posts.api.serializers import PostListSerializer, PostDetailSerializer
data = { 'title':"Yeah buddy","content":"New Content","publish":"2016-2-13"}

new_item = Pos
"""