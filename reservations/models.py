from django.db import models
from django.conf import settings

from books.models import Book


class Reservation(models.Model):

    class Status(models.TextChoices):
        WAITING = "WAITING", "Waiting"
        FULFILLED = "FULFILLED", "Fulfilled"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    fulfilled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                condition=models.Q(status="WAITING"),
                name="unique_active_reservation"
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"