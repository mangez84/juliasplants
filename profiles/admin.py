from django.contrib import admin
from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'postcode', 'country',)
    ordering = ('user',)


admin.site.register(UserProfile, ProfileAdmin)
