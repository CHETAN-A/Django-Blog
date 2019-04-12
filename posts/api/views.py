from django.db.models import Q
from rest_framework.generics import  ( ListAPIView, RetrieveAPIView,
									 UpdateAPIView, DestroyAPIView,
									 CreateAPIView, RetrieveUpdateAPIView )
from rest_framework.filters import ( SearchFilter, OrderingFilter)
from .pagination import (PostLimitOffsetPagination, PostPageNumberPagination)
from posts.models import Post
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import ( AllowAny, IsAuthenticated,
										IsAdminUser, IsAuthenticatedOrReadOnly )
from .serializers import ( PostListSerializer, PostDetailSerializer,
							 PostCreateUpdateSerializer )


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
	# queryset = Post.objects.all()
	serializer_class = PostListSerializer
	filter_backends= [SearchFilter]
	search_fields = ('title','content','user__first_name')
	pagination_class = PostLimitOffsetPagination #PageNumberPagination

	def get_queryset(self,*args,**kwargs):
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	lookup_field = 'slug'

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'