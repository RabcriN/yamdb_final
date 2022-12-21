from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
        "category",
    )
    list_editable = ("description", "category")
    search_fields = ("name", "year", "genre", "category")
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_display_links = ("slug",)
    list_editable = ("name",)
    search_fields = ("name", "slug")


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "text",
        "pub_date",
    )
    list_editable = ("text",)
    search_fields = ("author", "text", "pub_date", "title", "score")


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "text",
        "pub_date",
        "review",
    )
    list_editable = ("text",)
    search_fields = ("author", "text", "pub_date", "review")


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_display_links = ("slug",)
    list_editable = ("name",)
    search_fields = ("name", "slug")


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
