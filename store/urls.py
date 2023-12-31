from django.urls import path

from . import views

urlpatterns = [
    path("", views.store_view, name="store_view"),
    path("products/", views.products_view, name="products_view"),
    path("products/<int:pk>/", views.product_item_view, name="product_item_view"),
    path("clients/", views.clients_view, name="clients_view"),
    path("clients/<int:pk>/", views.client_item_view, name="client_item_view"),
    path("orders/", views.orders_view, name="orders_view"),
    # put this before the next route, otherwise it will remove order as well
    path("orders/<int:pk>/", views.order_item_view, name="order_item_view"),

    # htmx endpoints
    path("hx-remove-order-item/<int:pk>/", views.hx_remove_order_item, name="hx_remove_order_item"),
    path("hx-search-items/", views.hx_search_items, name="hx_search_items"),
]
