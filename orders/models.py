from django.db import models


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

    def __str__(self):
        return f"Заказ {self.id} (Стол {self.table_number}) - {self.get_status_display()}"

    def calculate_total(self):
        """Метод для автоматического расчета общей стоимости заказа."""
        self.total_price = sum(item['price'] for item in self.items)
        self.save()


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
