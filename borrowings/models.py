from django.db import models
from django.conf import settings
from django.utils import timezone

from books.models import Book


class BorrowRecord(models.Model):

    class Status(models.TextChoices):
        BORROWED = "BORROWED", "Borrowed"
        RETURNED = "RETURNED", "Returned"
        OVERDUE = "OVERDUE", "Overdue"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrow_records"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrow_records"
    )

    borrowed_at = models.DateTimeField(
        auto_now_add=True
    )

    due_date = models.DateTimeField()

    returned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BORROWED
    )

    fine = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"

    @property
    def is_overdue(self):
        return (
            self.status == self.Status.BORROWED
            and timezone.now() > self.due_date
        )