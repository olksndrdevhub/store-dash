from django.urls import path

from . import views

urlpatterns = [
    path('', views.store_view, name='store_view'),
    path('products/', views.products_view, name='products_view'),
    path('products/<int:id>/', views.product_item_view, name='product_item_view'),
    path('clients/', views.clients_view, name='clients_view'),
    path('orders/', views.orders_view, name='orders_view'),
]