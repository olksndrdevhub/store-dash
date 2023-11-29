from decimal import Decimal
from django.db import models


# Create your models here.
class Product(models.Model):
    sku = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product_images", blank=True, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, null=True
    )
    color = models.ForeignKey("Color", on_delete=models.CASCADE, blank=True, null=True)
    available_quantity = models.IntegerField(default=0, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return str(self.name)


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Colors"

    def __str__(self) -> str:
        return str(self.name)


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    delivery_address = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.email}"


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField(default=1)
    ordered_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def cost(self):
        return self.ordered_price * Decimal(self.quantity)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PLACED = 'PL', 'Placed'
        PROCESSING = 'PR', 'Processing'
        COMPLETED = 'CO', 'Completed'
        CANCELLED = 'CA', 'Cancelled'

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=OrderStatus.choices, default=OrderStatus.PLACED)

    def __str__(self):
        return f"Order {self.id}, {self.created}, payed: {self.payment_completed}"

    @property
    def total_cost(self):
        cost = 0.0
        for item in self.items.all():
            cost += item.cost
        return cost
