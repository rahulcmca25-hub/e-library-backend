from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "description",
            "author",
            "category",
            "total_copies",
            "available_copies",
            "published_date",
            "created_at",
            "updated_at",
        ]