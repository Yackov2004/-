from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Order
from decimal import Decimal
from django.db import models

class OrderViewTests(TestCase):
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

    def test_order_list_view(self):
        """Test the order list view"""
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertContains(response, 'Борщ')

    def test_order_create_view(self):
        """Test creating a new order"""
        data = {
            'table_number': '7',
            'items[]': ['Пицца', 'Суп'],
            'prices[]': ['550', '300']
        }
        response = self.client.post(reverse('order_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Order.objects.count(), 2)
        new_order = Order.objects.latest('id')
        self.assertEqual(new_order.table_number, 7)
        self.assertEqual(len(new_order.items), 2)

    def test_order_update_view(self):
        """Test updating an existing order"""
        data = {
            'table_number': '8',
            'items[]': ['Новое блюдо'],
            'prices[]': ['400'],
            'status': 'ready'
        }
        response = self.client.post(
            reverse('order_update', args=[self.order.id]), 
            data
        )
        self.assertEqual(response.status_code, 302)
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.table_number, 8)
        self.assertEqual(updated_order.status, 'ready')

    def test_order_delete_view(self):
        """Test deleting an order"""
        response = self.client.get(
            reverse('order_delete', args=[self.order.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)

    def test_calculate_revenue_view(self):
        """Test revenue calculation"""
        # Create multiple orders with different statuses
        paid_order1 = Order.objects.create(
            table_number=10,
            items=[{'name': 'Стейк', 'price': 1500}],
            status='paid'
        )
        paid_order1.calculate_total()

        paid_order2 = Order.objects.create(
            table_number=11,
            items=[{'name': 'Борщ', 'price': 350}, {'name': 'Десерт', 'price': 250}],
            status='paid'
        )
        paid_order2.calculate_total()

        # Create unpaid order that shouldn't be counted
        pending_order = Order.objects.create(
            table_number=12,
            items=[{'name': 'Салат', 'price': 400}],
            status='pending'
        )
        pending_order.calculate_total()

        ready_order = Order.objects.create(
            table_number=13,
            items=[{'name': 'Пицца', 'price': 800}],
            status='ready'
        )
        ready_order.calculate_total()

        response = self.client.get(reverse('calculate_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/revenue.html')
        
        # Total should be sum of only paid orders (1500 + 350 + 250 = 2100)
        self.assertContains(response, '2100')
        
        # Verify that unpaid orders are not included
        self.assertEqual(Order.objects.filter(status='paid').count(), 2)
        total_revenue = Order.objects.filter(status='paid').aggregate(
            total=models.Sum('total_price'))['total']
        self.assertEqual(float(total_revenue), 2100.0)

    def test_zero_revenue(self):
        """Test revenue calculation when there are no paid orders"""
        # Create only unpaid orders
        Order.objects.create(
            table_number=1,
            items=[{'name': 'Салат', 'price': 400}],
            status='pending'
        ).calculate_total()

        Order.objects.create(
            table_number=2,
            items=[{'name': 'Суп', 'price': 300}],
            status='ready'
        ).calculate_total()

        response = self.client.get(reverse('calculate_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/revenue.html')
        self.assertContains(response, '0')  # Should show zero revenue
