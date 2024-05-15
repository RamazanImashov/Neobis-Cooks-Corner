from django.contrib import admin
from .models import UserProfile

# Register your models here.


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "username", "profile_image"]
    # readonly_fields = ["activation_code", "is_active"]
