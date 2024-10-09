from django import forms
from django.contrib.auth.models import User
from ProjectWebGame.models import UserProfileInfo, Game

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
        fields = ['name', 'description', 'developer']