from django import forms
from django.forms import ModelForm, Textarea, widgets
from .models import User, Post

class CreateNewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description']
        widgets = {
            'description': Textarea(attrs={'class': 'form-control', 'rows' : 10})
        }