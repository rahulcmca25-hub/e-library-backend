from django.db import models

from books.models import Book


class BookSummary(models.Model):

    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name="ai_summary"
    )

    summary = models.TextField()

    key_points = models.JSONField(
        default=list
    )

    target_audience = models.CharField(
        max_length=255,
        blank=True
    )

    model_name = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"AI Summary - {self.book.title}"