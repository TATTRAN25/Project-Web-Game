from django.contrib import admin
from .models import UserProfileInfo, Developer, Category, Game, Review, Draft

@admin.register(UserProfileInfo)
class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'bio', 'avatar')
    search_fields = ('user__username', 'address')

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'developer', 'category', 'release_date', 'is_published')
    list_filter = ('developer', 'category', 'is_published')
    search_fields = ('name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'is_published', 'created_at')
    list_filter = ('game', 'is_published')
    search_fields = ('content',)

admin.site.register(Draft)