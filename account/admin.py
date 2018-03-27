from django.contrib import admin
from .models import UserProfile, Userinfo


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'brith', 'phone')
    list_filter = ('phone',)


class UserinfoAdmin(admin.ModelAdmin):
    list_display = ('user',  'profession', 'school', 'company', 'aboutme', 'photo')
    list_filter = ('school', 'company', 'profession')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Userinfo, UserinfoAdmin)
