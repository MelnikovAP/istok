from django.contrib import admin
from .models import Stand

@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "group_name", "source", "is_active")
    list_filter = ("is_active", "source")
    search_fields = ("title", "slug", "group_name", "view_path", "upstream_url")
    prepopulated_fields = {"slug": ("title",)}