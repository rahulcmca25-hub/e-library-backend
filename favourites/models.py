from django.db import models
from django.conf import settings

from books.models import Book


class Favourite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="favourited_by"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_user_favourite"
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"