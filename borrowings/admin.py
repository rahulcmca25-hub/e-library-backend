from django.contrib import admin

from .models import BorrowRecord


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "book",
        "borrowed_at",
        "due_date",
        "returned_at",
        "status",
        "fine",
    )

    list_filter = (
        "status",
        "borrowed_at",
        "due_date",
    )

    search_fields = (
        "user__email",
        "book__title",
    )

    ordering = (
        "-borrowed_at",
    )