from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='user_pic', blank=True)

    def __str__(self):
        return self.user.username

class Developer(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='studio_pic', blank=True)

    def __str__(self):  
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=255)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='game_pic/', blank=True)
    link_dowload = models.URLField(blank=True)
    release_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    rating = models.FloatField(null=True, validators=[MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} đánh giá {self.game}"
    
class Draft(models.Model):

    title = models.CharField(max_length=200)

    content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title