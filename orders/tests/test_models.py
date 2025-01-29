from django.test import TestCase
from orders.models import Order
from decimal import Decimal

class OrderModelTests(TestCase):
    def setUp(self):
        self.order_data = {
            'table_number': 5,
            'items': [
                {'name': 'Борщ', 'price': 350},
                {'name': 'Салат', 'price': 250}
            ],
            'status': 'pending'
        }
        self.order = Order.objects.create(**self.order_data)
        self.order.calculate_total()

    def test_order_creation(self):
        """Test that an order is created with correct data"""
        self.assertEqual(self.order.table_number, 5)
        self.assertEqual(len(self.order.items), 2)
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.total_price, Decimal('600.00'))

    def test_calculate_total(self):
        """Test total price calculation"""
        order = Order.objects.create(
            table_number=1,
            items=[{'name': 'Тест', 'price': 100}],
            status='pending'
        )
        order.calculate_total()
        self.assertEqual(order.total_price, Decimal('100.00'))
