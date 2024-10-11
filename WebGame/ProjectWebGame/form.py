from django import forms
from django.contrib.auth.models import User
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

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
<<<<<<< HEAD
        exclude = ['release_date','created_at', 'updated_at', 'is_published']
            
            
=======
        fields = ['name', 'description', 'developer', 'image', 'link_dowload', 'release_date']

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'description', 'website', 'logo']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
>>>>>>> django/3-TAT
