from django.test import TestCase, Client
from orders.models import Order
import json

class OrderAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.order_data = {
            'table_number': 3,
            'items': [
                {'name': 'Борщ', 'price': 350},
                {'name': 'Салат', 'price': 250}
            ],
            'status': 'pending'
        }
        self.order = Order.objects.create(**self.order_data)
        self.order.calculate_total()

    def test_api_list_orders(self):
        """Test API endpoint for listing orders"""
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['table_number'], 3)

    def test_api_create_order(self):
        """Test API endpoint for creating an order"""
        new_order_data = {
            'table_number': 5,
            'items': [{'name': 'Пицца', 'price': 550}],
            'status': 'pending'
        }
        response = self.client.post(
            '/orders/',
            data=json.dumps(new_order_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 2)

    def test_api_update_order(self):
        """Test API endpoint for updating an order"""
        updated_data = {
            'table_number': 7,
            'items': [{'name': 'Суп', 'price': 300}],
            'status': 'ready'
        }
        response = self.client.put(
            f'/orders/{self.order.id}/',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.table_number, 7)
        self.assertEqual(updated_order.status, 'ready')

    def test_api_delete_order(self):
        """Test API endpoint for deleting an order"""
        response = self.client.delete(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Order.objects.count(), 0)
