from django.contrib import admin
from .models import Stand

@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "group_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "slug", "group_name")
    prepopulated_fields = {"slug": ("title",)}