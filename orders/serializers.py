from rest_framework import serializers
from typing import Any, Dict, List
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields: str = '__all__'

    def to_representation(self, instance: Order) -> Dict[str, Any]:
        return super().to_representation(instance)

    def create(self, validated_data: Dict[str, Any]) -> Order:
        return super().create(validated_data)

    def update(self, instance: Order, validated_data: Dict[str, Any]) -> Order:
        return super().update(instance, validated_data)
