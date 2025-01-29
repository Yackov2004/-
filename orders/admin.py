from django.contrib import admin
from typing import List, Tuple
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = ('id', 'table_number', 'total_price', 'status')
    list_filter: Tuple[str, ...] = ('status',)
    search_fields: Tuple[str, ...] = ('table_number',)
