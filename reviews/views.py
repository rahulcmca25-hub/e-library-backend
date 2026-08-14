from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        book_id = request.query_params.get("book")

        reviews = Review.objects.all()

        if book_id:
            reviews = reviews.filter(
                book_id=book_id
            )

        serializer = ReviewSerializer(
            reviews,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ReviewSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )