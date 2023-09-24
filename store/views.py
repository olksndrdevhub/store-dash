from django.shortcuts import render
from django.contrib import messages

from .models import Product, Category, Color
from account.models import User


# Create your views here.
def store_view(request):
    context = {}
    user: User = request.user

    return render(request, 'store.html', context)


def products_view(request):
    context: dict = {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
    }

    if request.method == 'POST' and request.htmx:
        category: str = request.POST.get('category', None)
        color: str = request.POST.get('color', None)
        name: str = request.POST.get('name', None)
        price: str = request.POST.get('price', 0.0)
        available_quantity: str = request.POST.get('available_quantity', 0)

        if name is None or name.strip() == '':
            messages.add_message(
                request,
                messages.ERROR,
                "Product name is required!"
            )
            return render(request, 'products.html', context)
        new_product = Product.objects.create(
            name=name.strip(),
            price=int(price),
        )
        if category and category.strip() != '':
            new_product.category = Category.objects.get(name=category)
        if color and color.strip() != '':
            new_product.color = Color.objects.get(name=color)
        if available_quantity and available_quantity.strip() != '':
            new_product.available_quantity = int(available_quantity)
        new_product.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Product created successfully!"
        )
        context['products'] = Product.objects.all()

    return render(request, 'products.html', context)


def product_item_view(request, pk):
    context: dict = {
        'product': Product.objects.get(pk=pk),
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
    }

    if request.htmx:
        return render(request, 'partials/editProductForm.html', context)

    context['products'] = Product.objects.all()
    return render(request, 'products.html', context)


def clients_view(request):
    context: dict = {}
    user: User = request.user

    return render(request, 'clients.html', context)


def orders_view(request):
    context: dict = {}
    user: User = request.user

    return render(request, 'orders.html', context)
