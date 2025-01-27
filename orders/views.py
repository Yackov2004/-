from rest_framework import viewsets
from .serializers import OrderSerializer
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from django.db import models


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_create(request):
    if request.method == 'POST':
        # Получаем данные из формы
        table_number = request.POST.get('table_number')
        # Ожидаем список блюд в формате JSON
        items = request.POST.getlist('items[]')
        item_prices = request.POST.getlist('prices[]')  # Цены на блюда

        # Преобразуем данные в формат JSON
        formatted_items = [
            {'name': name, 'price': float(price)}
            for name, price in zip(items, item_prices)
        ]

        # Создаем заказ
        order = Order.objects.create(
            table_number=table_number,
            items=formatted_items
        )
        order.calculate_total()  # Рассчитываем общую стоимость заказа

        return redirect('order_list')

    return render(request, 'orders/order_create.html')


def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')


def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Обновляем данные заказа
        order.table_number = request.POST.get('table_number')
        items = request.POST.getlist('items[]')
        item_prices = request.POST.getlist('prices[]')

        # Преобразуем данные в формат JSON
        formatted_items = [
            {'name': name, 'price': float(price)}
            for name, price in zip(items, item_prices)
        ]
        order.items = formatted_items
        order.calculate_total()  # Пересчитываем общую стоимость
        order.status = request.POST.get('status')
        order.save()

        return redirect('order_list')

    return render(request, 'orders/order_update.html', {'order': order})


def calculate_revenue(request):
    # Суммируем total_price для всех оплаченных заказов
    total_revenue = Order.objects.filter(status='paid').aggregate(
        total=Sum('total_price'))['total'] or 0

    return render(request, 'orders/revenue.html', {'total_revenue': total_revenue})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Все заказы
    serializer_class = OrderSerializer  # Используем созданный сериализатор
