# projects/models.py (добавь поля)
from django.db import models

class Stand(models.Model):
    SOURCE_CHOICES = [
        ("internal", "Internal"),
        ("external", "External"),
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    group_name = models.CharField(max_length=50, help_text="Имя группы, которая даёт доступ (например, sub_h2lab)")

    source = models.CharField(max_length=16, choices=SOURCE_CHOICES, default="internal")
    view_path = models.CharField(max_length=255, blank=True) 
    upstream_url = models.URLField(blank=True)          


    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
