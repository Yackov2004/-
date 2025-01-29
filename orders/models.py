from django.db import models
from typing import List, Dict, Any, cast
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]
    table_number = models.IntegerField()
    items = models.JSONField()  # Список блюд и цен в формате JSON
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self) -> str:
        return f"Заказ {self.id} (Стол {self.table_number}) - {self.get_status_display()}"

    def calculate_total(self) -> None:
        """Метод для автоматического расчета общей стоимости заказа."""
        self.total_price = sum(Decimal(str(item['price'])) for item in self.items)
        self.save()


class Item(models.Model):
    name: str = models.CharField(max_length=255)
    price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name
