from django.contrib import admin
from django.utils.html import format_html
from ProjectWebGame.models import UserProfileInfo

# Đăng ký model với admin
class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')  
    ordering = ['id'] 
    search_fields = ['user__username']  
    list_per_page = 20  

    def username(self, obj):
        return obj.user.username 

    def profile_pic_display(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.profile_pic.url)
        return "No Image"

    username.short_description = 'Username'  
    profile_pic_display.short_description = 'Profile Picture'

# Đăng ký model với admin
admin.site.register(UserProfileInfo, UserProfileInfoAdmin)