from django.contrib import admin
from .models import UserProfile, UserProfileComment


class UserProfileAdmin(admin.ModelAdmin):
    """Display user profiles on the admin site."""
    list_display = ('user', 'address', 'city', 'postcode', 'country',)
    ordering = ('user',)


class UserProfileCommentAdmin(admin.ModelAdmin):
    """Display user profile comments on the admin site."""
    list_display = ('title', 'comment', 'rating', 'profile',)
    ordering = ('profile',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfileComment, UserProfileCommentAdmin)
