from django.contrib import admin

from .models import Author, Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "date", "tags")
    list_display = ("title", "date", "author")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
