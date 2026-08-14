from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import BorrowRecord
from .serializers import BorrowRecordSerializer
from books.models import Book


MAX_ACTIVE_BORROWS = 3
BORROW_DAYS = 14
FINE_PER_DAY = Decimal("5.00")


class BorrowBookView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        book_id = request.data.get("book_id")

        if not book_id:
            return Response(
                {"detail": "book_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            with transaction.atomic():

                book = Book.objects.select_for_update().get(
                    id=book_id
                )

                # --------------------------------
                # CHECK AVAILABLE COPIES
                # --------------------------------

                if book.available_copies <= 0:

                    return Response(
                        {"detail": "Book is currently unavailable"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # --------------------------------
                # CHECK MAXIMUM ACTIVE BORROWS
                # --------------------------------

                active_count = BorrowRecord.objects.filter(
                    user=request.user,
                    status=BorrowRecord.Status.BORROWED
                ).count()

                if active_count >= MAX_ACTIVE_BORROWS:

                    return Response(
                        {
                            "detail": (
                                "You can borrow maximum "
                                f"{MAX_ACTIVE_BORROWS} books at a time"
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # --------------------------------
                # CHECK DUPLICATE ACTIVE BORROW
                # --------------------------------

                already_borrowed = BorrowRecord.objects.filter(
                    user=request.user,
                    book=book,
                    status=BorrowRecord.Status.BORROWED
                ).exists()

                if already_borrowed:

                    return Response(
                        {
                            "detail":
                            "You have already borrowed this book"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # --------------------------------
                # CREATE BORROW RECORD
                # --------------------------------

                due_date = (
                    timezone.now()
                    + timedelta(days=BORROW_DAYS)
                )

                borrow_record = BorrowRecord.objects.create(
                    user=request.user,
                    book=book,
                    due_date=due_date,
                    status=BorrowRecord.Status.BORROWED
                )

                # --------------------------------
                # DECREASE AVAILABLE COPIES
                # --------------------------------

                book.available_copies -= 1
                book.save(update_fields=["available_copies"])

            serializer = BorrowRecordSerializer(
                borrow_record
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Book.DoesNotExist:

            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ReturnBookView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            with transaction.atomic():

                borrow = BorrowRecord.objects.select_for_update().get(
                    pk=pk,
                    user=request.user,
                    status=BorrowRecord.Status.BORROWED
                )

                # --------------------------------
                # CALCULATE FINE
                # --------------------------------

                now = timezone.now()

                fine = Decimal("0.00")

                if now > borrow.due_date:

                    overdue_seconds = (
                        now - borrow.due_date
                    ).total_seconds()

                    overdue_days = int(
                        overdue_seconds // (24 * 60 * 60)
                    ) + 1

                    fine = (
                        Decimal(overdue_days)
                        * FINE_PER_DAY
                    )

                # --------------------------------
                # RETURN BOOK
                # --------------------------------

                borrow.returned_at = now
                borrow.status = BorrowRecord.Status.RETURNED
                borrow.fine = fine

                borrow.save()

                # --------------------------------
                # INCREASE AVAILABLE COPIES
                # --------------------------------

                book = Book.objects.select_for_update().get(
                    id=borrow.book.id
                )

                book.available_copies += 1
                book.save(
                    update_fields=["available_copies"]
                )

            serializer = BorrowRecordSerializer(
                borrow
            )

            return Response(serializer.data)

        except BorrowRecord.DoesNotExist:

            return Response(
                {
                    "detail":
                    "Active borrowing record not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class BorrowHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        records = BorrowRecord.objects.filter(
            user=request.user
        ).order_by("-borrowed_at")

        serializer = BorrowRecordSerializer(
            records,
            many=True
        )

        return Response(serializer.data)


class OverdueBooksView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        records = BorrowRecord.objects.filter(
            user=request.user,
            status=BorrowRecord.Status.BORROWED,
            due_date__lt=timezone.now()
        )

        data = []

        for record in records:

            overdue_seconds = (
                timezone.now() - record.due_date
            ).total_seconds()

            overdue_days = int(
                overdue_seconds // (24 * 60 * 60)
            ) + 1

            fine = (
                Decimal(overdue_days)
                * FINE_PER_DAY
            )

            data.append({
                "id": record.id,
                "book": record.book.title,
                "due_date": record.due_date,
                "overdue_days": overdue_days,
                "current_fine": fine
            })

        return Response(data)