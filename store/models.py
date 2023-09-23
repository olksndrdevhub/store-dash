from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return str(self.name)


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Colors'

    def __str__(self) -> str:
        return str(self.name)
