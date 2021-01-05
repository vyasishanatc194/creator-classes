from rest_framework import serializers
from ..models import User


class CardSerializer(serializers.ModelSerializer):
    """Serializes the Card data into JSON"""
    class Meta:
        model = User
        fields = (
            "id",
            "card_id",
            "customer_id",
            "brand",
            "exp_month",
            "exp_year",
            "last4",
            "card_name",
        )
