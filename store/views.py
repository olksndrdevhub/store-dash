from django.shortcuts import render

from .models import Product, Category, Color
from account.models import User


# Create your views here.
def store_view(request):
    context = {}
    user: User = request.user

    return render(request, 'store.html', context)


def products_view(request):
    context: dict = {}

    products = Product.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()

    context['products'] = products
    context['categories'] = categories
    context['colors'] = colors
    return render(request, 'products.html', context)

def product_item_view(request, id):
    context: dict = {}
    user: User = request.user
    product: Product = Product.objects.get(id=id)
    products = Product.objects.all()

    context['product'] = product
    context['products'] = products
    return render(request, 'products.html', context)


def clients_view(request):
    context: dict = {}
    user: User = request.user

    return render(request, 'clients.html', context)


def orders_view(request):
    context: dict = {}
    user: User = request.user

    return render(request, 'orders.html', context)
