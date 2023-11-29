from django.urls import path

from . import views

urlpatterns = [
    path("", views.store_view, name="store_view"),
    path("products/", views.products_view, name="products_view"),
    path("products/<int:pk>/", views.product_item_view, name="product_item_view"),
    path("clients/", views.clients_view, name="clients_view"),
    path("clients/<int:pk>/", views.client_item_view, name="client_item_view"),
    path("orders/", views.orders_view, name="orders_view"),

    path("hx-search-clients/", views.hx_search_clients, name="hx_search_clients"),
]
