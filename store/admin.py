from django.contrib import admin

from .models import Product, Category, Color

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'color', 'available_quantity',
                    'created', 'updated')
    list_filter = ('category', 'color',)
    # list_editable = ('price',)
    search_fields = ('name', 'category', 'color')
    date_hierarchy = 'created'
    ordering = ('-created',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
