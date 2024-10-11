from django import forms
from django.contrib.auth.models import User
<<<<<<< HEAD
from ProjectWebGame.models import UserProfileInfo, Game
from .models import Post, Comment
=======
from ProjectWebGame.models import UserProfileInfo, Game, Developer, Category
>>>>>>> django/3-TAT

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['address', 'bio', 'avatar']

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'developer', 'image', 'link_dowload', 'release_date']

<<<<<<< HEAD
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
=======
class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'description', 'website', 'logo']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
>>>>>>> django/3-TAT
