from django.core.management.base import BaseCommand
from orders.models import Order
from typing import Any, Dict
import random

class Command(BaseCommand):
    help = 'Generates mock data for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of orders to generate')

    def handle(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        count = int(kwargs['count'])
        
        # Sample menu items
        menu_items: List[Dict[str, Any]] = [
            {"name": "Борщ", "price": 350},
            {"name": "Цезарь с курицей", "price": 420},
            {"name": "Стейк Рибай", "price": 1500},
            {"name": "Паста Карбонара", "price": 450},
            {"name": "Суп грибной", "price": 300},
            {"name": "Пицца Маргарита", "price": 550},
            {"name": "Салат Греческий", "price": 380},
            {"name": "Тирамису", "price": 280},
            {"name": "Капучино", "price": 180},
            {"name": "Лимонад", "price": 150},
        ]

        statuses: List[str] = ['pending', 'ready', 'paid']

        for i in range(count):
            num_items: int = random.randint(1, 5)
            order_items: List[Dict[str, Any]] = random.sample(menu_items, num_items)
            
            order: Order = Order.objects.create(
                table_number=random.randint(1, 20),
                items=order_items,
                status=random.choice(statuses)
            )
            order.calculate_total()

            self.stdout.write(
                self.style.SUCCESS(f'Created order #{order.id} for table {order.table_number}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} orders')
        )
