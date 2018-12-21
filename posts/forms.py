from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
	"""docstring for PostForm"""
	publish = forms.DateField(widget= forms.SelectDateWidget)
	content = forms.CharField(widget= PagedownWidget(show_preview=False))
	class Meta:
		"""docstring for Meta"""
		model = Post
		fields = ["title","content","image","draft","publish"]
			
