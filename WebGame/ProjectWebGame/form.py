from django import forms
from django.contrib.auth.models import User
from ProjectWebGame.models import UserProfileInfo, Game
from .models import Comment, ReplyComment
from ProjectWebGame.models import UserProfileInfo, Game, Developer, Category

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['address', 'bio', 'avatar']

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['release_date','created_at', 'updated_at', 'is_published']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea', 'rows': 1, 'style': 'resize: none; height: auto;', 'name': 'text'}),
        }
        
class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = ReplyComment
        fields = ['text']

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'description', 'website', 'logo']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'margin-bottom: 1rem'}),
        }
