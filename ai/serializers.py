from rest_framework import serializers

from .models import BookSummary


class BookSummarySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = BookSummary

        fields = [
            "id",
            "book",
            "summary",
            "key_points",
            "target_audience",
            "model_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields