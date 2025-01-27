from rest_framework import serializers
from .models import Order  # Импортируем модель Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order  # Модель, для которой будет сериализатор
        fields = '__all__'  # Все поля модели включаем в сериализатор
