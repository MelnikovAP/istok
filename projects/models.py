from django.db import models

class Stand(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    group_name = models.CharField(max_length=50, help_text="Имя группы, которая даёт доступ (например, sub_h2lab)")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title