from time import sleep
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category, Color
from account.models import User


def get_paginated_query(query, request, item=None):
    '''
    helper function to generate paginated query
    '''
    paginator = Paginator(query, 10)
    if item:
        # Calculate the page number by finding the index of the item in the list and dividing by the page size
        item_index = list(query).index(item)
        page_number = (item_index // 5) + 1
    else:
        page_number = request.GET.get('page', 1)
    try:
        query = paginator.page(page_number)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        query = paginator.page(1)

    page_range = paginator.get_elided_page_range(
        number=query.number,
        on_each_side=3,
        on_ends=1
    )
    return query, page_range


# Create your views here.
def store_view(request):
    context = {}
    user: User = request.user

    return render(request, 'store.html', context)


def products_view(request):
    context: dict = {
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
    }
    products = Product.objects.all()

    if 'search' in request.GET and request.GET.get('search').strip() != '':
        context['search'] = request.GET.get('search')
        products = products.filter(name__icontains=request.GET.get('search'))

    context['products'], context['page_range'] = get_paginated_query(
        products,
        request
    )


    if request.method == 'POST' and request.htmx:
        data = request.POST
        print(data)
        name: str = data.get('name', '')
        price_str: str = data.get('price', '0.0')
        category: str = data.get('category', '')
        color: str = data.get('color', '')
        available_quantity: str = data.get('available_quantity', '0')
        sku: str = data.get('sku', '')

        if name is None or name.strip() == '':
            messages.add_message(
                request,
                messages.ERROR,
                "Product name is required!"
            )
            return render(request, 'products.html', context)
        if price_str.strip() == '':
            price_str = '0.0'
        price = float(price_str)
        new_product = Product.objects.create(
            name=name.strip(),
            price=price,
        )
        if category.strip() != '' and Category.objects.filter(name=category).exists():
            new_product.category = Category.objects.get(name=category)
        if color.strip() != '' and Color.objects.filter(name=color).exists():
            new_product.color = Color.objects.get(name=color)
        if available_quantity.strip() == '':
            available_quantity = '0'
        new_product.available_quantity = int(available_quantity)
        if sku.strip() != '':
            new_product.sku = sku.strip()
        new_product.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Product created successfully!"
        )
        context['products'], context['page_range'] = get_paginated_query(
            Product.objects.all(),
            request
        )

    return render(request, 'products.html', context)


def product_item_view(request, pk):
    context: dict = {
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
    }
    context['product'] = Product.objects.get(pk=pk)

    if request.htmx and request.method == 'DELETE':
        product: Product = context['product']
        product.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Product deleted successfully!"
        )
        context['products'], context['page_range'] = get_paginated_query(Product.objects.all(), request)
        response = render(request, 'products.html', context)
        return response

    if request.method == 'POST' and request.htmx:
        product: Product = context['product']
        data = request.POST
        print(data)
        name: str = data.get('name', '')
        price_str: str = data.get('price', '0.0')
        category: str = data.get('category', '')
        color: str = data.get('color', '')
        available_quantity: str = data.get('available_quantity', '0')
        sku: str = data.get('sku', '')
        if name is None or name.strip() == '':
            messages.add_message(
                request,
                messages.ERROR,
                "Product name is required!"
            )
            return render(request, 'partials/editProductForm.html', context)
        product.name = name.strip()
        if price_str.strip() == '':
            price_str = '0.0'
        product.price = float(price_str)
        if category.strip() != '' and Category.objects.filter(name=category).exists():
            product.category = Category.objects.get(name=category)
        if color.strip() != '' and Color.objects.filter(name=color).exists():
            product.color = Color.objects.get(name=color)
        if available_quantity.strip() == '':
            available_quantity = '0'
        product.available_quantity = int(available_quantity)
        if sku.strip() != '':
            product.sku = sku.strip()
        product.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Product updated successfully!"
        )
        messages.add_message(
            request,
            messages.WARNING,
            "Product updated successfully!"
        )
        messages.add_message(
            request,
            messages.ERROR,
            "Product updated successfully!"
        )
        return render(request, 'partials/editProductForm.html', context)

    return render(request, 'product_page.html', context)


def clients_view(request):
    context: dict = {}
    user: User = request.user

    return render(request, 'clients.html', context)


def orders_view(request):
    context: dict = {}
    user: User = request.user

    return render(request, 'orders.html', context)
