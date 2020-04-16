from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comments
from django.core.paginator import Paginator

class Add_Post(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    class Meta:
        model = Post
        fields=['title','content']

class Add_Comment(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    class Meta:
        model = Comments
        fields=['content']

class Search_Post(forms.Form):
    search_post = forms.CharField(max_length=100)
