from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='user_pic', blank=True)
    is_vip_requested = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)  # Trường theo dõi trạng thái VIP

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

class Draft(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title    
    
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    game = models.ForeignKey(Game, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    rating = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")
    
    def __str__(self):
        return f'Comment by {self.author.username}'
    
class ReplyComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.author.username} on {self.comment}'
    
