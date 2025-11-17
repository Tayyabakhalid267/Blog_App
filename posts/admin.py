from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'author', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('author',)

    def short_text(self, obj):
        return obj.text[:50]
    short_text.short_description = 'Text'
