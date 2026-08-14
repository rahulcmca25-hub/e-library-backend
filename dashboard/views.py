from django.contrib.auth import get_user_model
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from books.models import Book
from borrowings.models import BorrowRecord


User = get_user_model()


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            return Response(
                {"detail": "Only admin or librarian can access dashboard"},
                status=403
            )

        total_users = User.objects.count()
        total_books = Book.objects.count()

        total_copies = sum(
            Book.objects.values_list(
                "total_copies",
                flat=True
            )
        )

        available_copies = sum(
            Book.objects.values_list(
                "available_copies",
                flat=True
            )
        )

        active_borrowings = BorrowRecord.objects.filter(
            status=BorrowRecord.Status.BORROWED
        ).count()

        returned_books = BorrowRecord.objects.filter(
            status=BorrowRecord.Status.RETURNED
        ).count()

        overdue_books = BorrowRecord.objects.filter(
            status=BorrowRecord.Status.OVERDUE
        ).count()

        total_fines = BorrowRecord.objects.aggregate(
            total=Sum("fine")
        )["total"] or 0

        return Response({
            "total_users": total_users,
            "total_books": total_books,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "active_borrowings": active_borrowings,
            "returned_books": returned_books,
            "overdue_books": overdue_books,
            "total_fines": total_fines,
        })