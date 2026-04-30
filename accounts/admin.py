from django.contrib import admin
from .models import FrontendAuthToken


@admin.register(FrontendAuthToken)
class FrontendAuthTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "last_used_at")
    search_fields = ("user__username", "user__email", "key")
    readonly_fields = ("key", "created_at", "last_used_at")
