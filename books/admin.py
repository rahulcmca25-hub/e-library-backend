from django.contrib import admin

from .models import Author, Category, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "isbn",
        "author",
        "category",
        "total_copies",
        "available_copies",
        "published_date",
    )

    list_filter = (
        "category",
        "author",
    )

    search_fields = (
        "title",
        "isbn",
        "author__name",
    )

    ordering = (
        "title",
    )