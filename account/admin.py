from django.contrib import admin
from .models import UserProfile


# Register your models here.
class UserProfileAmin(admin.ModelAdmin):
    list_display = ('user', 'brith', 'phone')
    list_filter = ('phone',)


admin.site.register(UserProfile, UserProfileAmin)
