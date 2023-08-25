from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.auto_kiekis, name='car-quant'),
    path('cars/<int:car_id>', views.customer_car, name='car-one'),
    path('services/', views.services, name='services'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<uuid:pk>', views.OrderDetailView.as_view(), name='order-one'),
    path('search/', views.search, name='search'),
]

