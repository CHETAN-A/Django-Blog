from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
	message = 'YOu must be Owner of this Object'
	# my_safe_method = ['GET','PUT']

	# def has_permission(self,request,view):
	# 	if request.method in self.my_safe_method:
	# 		return True
			
	def has_object_permission(self,request,view,obj):
		if request.method in SAFE_METHODS:
			return True
		return obj.user == request.user