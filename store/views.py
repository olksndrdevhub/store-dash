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
    paginator = Paginator(query, 5)
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
    context['products'], context['page_range'] = get_paginated_query(
        Product.objects.all(),
        request
    )


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
            price=price,
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
        name: str = data.get('name', None)
        price: str = data.get('price', None)
        category: str = data.get('category', None)
        color: str = data.get('color', None)
        available_quantity: str = data.get('available_quantity', None)
        sku: str = data.get('sku', None)
        if name is None or name.strip() == '':
            messages.add_message(
                request,
                messages.ERROR,
                "Product name is required!"
            )
            return render(request, 'partials/editProductForm.html', context)
        product.name = name.strip()
        if price is None or price.strip() == '':
            messages.add_message(
                request,
                messages.ERROR,
                "Product price is required!"
            )
            return render(request, 'partials/editProductForm.html', context)
        product.price = price.strip()
        if category and category.strip() != '':
            product.category = Category.objects.get(name=category)
        if color and color.strip() != '':
            product.color = Color.objects.get(name=color)
        if available_quantity and available_quantity.strip() != '':
            product.available_quantity = int(available_quantity)
        if sku and sku.strip() != '':
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
