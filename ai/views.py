from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from books.models import Book

from .models import BookSummary
from .serializers import BookSummarySerializer
from .services import generate_book_summary


class BookSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        book = get_object_or_404(
            Book,
            pk=pk
        )

        # Return cached summary
        existing_summary = BookSummary.objects.filter(
            book=book
        ).first()

        if existing_summary:

            serializer = BookSummarySerializer(
                existing_summary
            )

            return Response({
                "cached": True,
                "data": serializer.data
            })

        try:

            result = generate_book_summary(book)

            summary = BookSummary.objects.create(
                book=book,
                summary=result["summary"],
                key_points=result["key_points"],
                target_audience=result["target_audience"],
                model_name="gpt-5-mini"
            )

            serializer = BookSummarySerializer(
                summary
            )

            return Response(
                {
                    "cached": False,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {
                    "detail": "AI summary generation failed",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookSummaryDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        summary = get_object_or_404(
            BookSummary,
            book_id=pk
        )

        serializer = BookSummarySerializer(
            summary
        )

        return Response(serializer.data)