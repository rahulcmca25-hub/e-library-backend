from rest_framework import serializers

from .models import BorrowRecord


class BorrowRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowRecord
        fields = [
            "id",
            "user",
            "book",
            "borrowed_at",
            "due_date",
            "returned_at",
            "status",
            "fine",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "user",
            "borrowed_at",
            "returned_at",
            "status",
            "fine",
            "created_at",
            "updated_at",
        ]