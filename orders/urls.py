from .views import OrderViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.urls import path
from . import views
# Создаем маршруты для API
router = DefaultRouter()
# 'orders' — это путь для API, по которому будут доступные все операции
router.register(r'orders', OrderViewSet)
urlpatterns = [
    # Главная страница со списком заказов
    path('', views.order_list, name='order_list'),
    path('', include(router.urls)),  # Включаем маршруты для API
    # Создание нового заказа
    path('add/', views.order_create, name='order_create'),
    path('<int:order_id>/delete/', views.order_delete,
         name='order_delete'),  # Удаление заказа
    path('<int:order_id>/update/', views.order_update,
         name='order_update'),  # Обновление заказа
    path('revenue/', views.calculate_revenue, name='calculate_revenue'),

]
