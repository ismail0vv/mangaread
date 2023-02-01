from django.contrib import admin
from users.models import User
from rest_framework_simplejwt import token_blacklist


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'nickname', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'nickname']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    list_per_page = 50


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)

admin.site.register(User, UserAdmin)
