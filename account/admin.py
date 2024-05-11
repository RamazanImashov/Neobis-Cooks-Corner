from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "activation_code", "is_active"]
    readonly_fields = ["activation_code", "is_active"]
