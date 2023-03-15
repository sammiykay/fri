from django.contrib import admin
from .models import *
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'image', 'facebook', 'linkedin', 'about_you', 'website_link']

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'agree']


class ContactUs(admin.ModelAdmin):
    list_display = ['name', 'email', 'body']


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Newsletter)
admin.site.register(PostDetail)
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Contact, ContactUs)