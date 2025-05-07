from django.contrib import admin
from .models import Profile
import admin_thumbnails
import datetime


# @admin_thumbnails.thumbnail('image')
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['registered_at', 'last_login']

    fieldsets = [
        ('Information', {'fields': ['username', 'email', 'image']}),
        ('Activity', {'fields': ['last_login', 'registered_at']}),
    ]
    list_display = ["username", "image", "email"]
    list_display_links = ["username", "email"]


admin.site.register(Profile,ProfileAdmin)
