from rest_framework import serializers

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation

        fields = [
            "id",
            "user",
            "book",
            "status",
            "created_at",
            "fulfilled_at",
        ]

        read_only_fields = [
            "user",
            "status",
            "created_at",
            "fulfilled_at",
        ]