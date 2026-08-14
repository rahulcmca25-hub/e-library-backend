from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from books.models import Book

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        reservations = Reservation.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = ReservationSerializer(
            reservations,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        book_id = request.data.get("book_id")

        if not book_id:
            return Response(
                {"detail": "book_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        book = get_object_or_404(
            Book,
            id=book_id
        )

        # Don't reserve an available book
        if book.available_copies > 0:
            return Response(
                {
                    "detail":
                    "Book is currently available. You can borrow it."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check existing waiting reservation
        existing = Reservation.objects.filter(
            user=request.user,
            book=book,
            status=Reservation.Status.WAITING
        ).exists()

        if existing:
            return Response(
                {
                    "detail":
                    "You already have an active reservation."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation = Reservation.objects.create(
            user=request.user,
            book=book
        )

        serializer = ReservationSerializer(
            reservation
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )