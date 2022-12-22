from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'nickname', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'nickname']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    list_per_page = 50


admin.site.register(User, UserAdmin)
