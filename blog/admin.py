from django.contrib import admin

from .models import Category, Comment, Post, PostPhoto


class PostPhotoInline(admin.StackedInline):
    model = PostPhoto


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at")
    search_fields = ("title",)
    filter_horizontal = ("categories",)
    inlines = (PostPhotoInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "published_at")
    search_fields = ("text", "post__title", "author__username")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")
