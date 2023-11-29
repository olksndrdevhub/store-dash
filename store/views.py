from django.shortcuts import render, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category, Color, Client, Order
from account.models import User


def get_paginated_query(query, request, item=None):
    """
    helper function to generate paginated query
    """
    paginator = Paginator(query, 10)
    if item:
        # Calculate the page number by finding the index of the item in the list and dividing by the page size
        item_index = list(query).index(item)
        page_number = (item_index // 5) + 1
    else:
        page_number = request.GET.get("page", 1)
    try:
        query = paginator.page(page_number)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        query = paginator.page(1)

    page_range = paginator.get_elided_page_range(
        number=query.number, on_each_side=3, on_ends=1
    )
    return query, page_range


# Create your views here.
@login_required
def store_view(request):
    context = {}
    user: User = request.user

    context["products"] = Product.objects.all().order_by("-created")[:5]
    context["products_count"] = Product.objects.all().count()
    context["out_of_stock_count"] = Product.objects.filter(available_quantity=0).count()

    context["clients"] = Client.objects.all().order_by("-created")[:5]
    context["clients_count"] = Client.objects.all().count()

    context["orders"] = Order.objects.all().order_by("-created")[:5]
    context["orders_count"] = Order.objects.all().count()
    context["completed_count"] = Order.objects.filter(completed=True).count()

    return render(request, "store.html", context)


@login_required
def products_view(request):
    context: dict = {
        "categories": Category.objects.all(),
        "colors": Color.objects.all(),
        "order_by": "-created",
    }
    products = Product.objects.all()

    if (
        "filter_category" in request.GET
        and request.GET.get("filter_category").strip() != ""
    ):
        context["filter_category"] = request.GET.get("filter_category")
        if request.GET.get("filter_category") == "all":
            pass
        elif request.GET.get("filter_category") == "none":
            products = products.filter(category__isnull=True)
        else:
            products = products.filter(
                category__name=request.GET.get("filter_category")
            )

    if "filter_color" in request.GET and request.GET.get("filter_color").strip() != "":
        context["filter_color"] = request.GET.get("filter_color")
        if request.GET.get("filter_color") == "all":
            pass
        elif request.GET.get("filter_color") == "none":
            products = products.filter(color__isnull=True)
        else:
            products = products.filter(color__name=request.GET.get("filter_color"))

    if "search" in request.GET and request.GET.get("search").strip() != "":
        context["search"] = request.GET.get("search")
        products = products.filter(name__icontains=request.GET.get("search"))

    if "order_by" in request.GET and request.GET.get("order_by").strip() != "":
        context["order_by"] = request.GET.get("order_by")
        products = products.order_by(request.GET.get("order_by"))

    context["products"], context["page_range"] = get_paginated_query(products, request)

    if request.method == "POST" and request.htmx:
        data = request.POST
        print(data)
        name: str = data.get("name", "")
        price_str: str = data.get("price", "0.0")
        category: str = data.get("category", "")
        color: str = data.get("color", "")
        available_quantity: str = data.get("available_quantity", "0")
        sku: str = data.get("sku", "")

        if name is None or name.strip() == "":
            messages.add_message(request, messages.ERROR, "Product name is required!")
            return render(request, "products.html", context)
        if price_str.strip() == "":
            price_str = "0.0"
        price = float(price_str)
        new_product = Product.objects.create(
            name=name.strip(),
            price=price,
        )
        if category.strip() != "" and Category.objects.filter(name=category).exists():
            new_product.category = Category.objects.get(name=category)
        if color.strip() != "" and Color.objects.filter(name=color).exists():
            new_product.color = Color.objects.get(name=color)
        if available_quantity.strip() == "":
            available_quantity = "0"
        new_product.available_quantity = int(available_quantity)
        if sku.strip() != "":
            new_product.sku = sku.strip()
        new_product.save()
        messages.add_message(request, messages.SUCCESS, "Product created successfully!")
        context["products"], context["page_range"] = get_paginated_query(
            Product.objects.all(), request
        )

    return render(request, "products.html", context)


@login_required
def product_item_view(request, pk):
    context: dict = {
        "categories": Category.objects.all(),
        "colors": Color.objects.all(),
    }
    context["product"] = Product.objects.get(pk=pk)

    if request.htmx and request.method == "DELETE":
        product: Product = context["product"]
        product.delete()
        messages.add_message(request, messages.SUCCESS, "Product deleted successfully!")
        context["products"], context["page_range"] = get_paginated_query(
            Product.objects.all(), request
        )
        response = render(request, "products.html", context)
        return response

    if request.method == "POST" and request.htmx:
        product: Product = context["product"]
        data = request.POST
        print(data)
        name: str = data.get("name", "")
        price_str: str = data.get("price", "0.0")
        category: str = data.get("category", "")
        color: str = data.get("color", "")
        available_quantity: str = data.get("available_quantity", "0")
        sku: str = data.get("sku", "")
        if name is None or name.strip() == "":
            messages.add_message(request, messages.ERROR, "Product name is required!")
            return render(request, "partials/editProductForm.html", context)
        product.name = name.strip()
        if price_str.strip() == "":
            price_str = "0.0"
        product.price = float(price_str)
        if category.strip() != "" and Category.objects.filter(name=category).exists():
            product.category = Category.objects.get(name=category)
        if color.strip() != "" and Color.objects.filter(name=color).exists():
            product.color = Color.objects.get(name=color)
        if available_quantity.strip() == "":
            available_quantity = "0"
        product.available_quantity = int(available_quantity)
        if sku.strip() != "":
            product.sku = sku.strip()
        product.save()
        messages.add_message(request, messages.SUCCESS, "Product updated successfully!")
        messages.add_message(request, messages.WARNING, "Product updated successfully!")
        messages.add_message(request, messages.ERROR, "Product updated successfully!")
        return render(request, "partials/editProductForm.html", context)

    response = render(request, "product_page.html", context)

    if not request.htmx and request.method == "GET":
        response.delete_cookie("prevUrl")
    return response


@login_required
def clients_view(request):
    context: dict = {}
    user: User = request.user
    clients = Client.objects.all()

    if "search" in request.GET and request.GET.get("search").strip() != "":
        context["search"] = request.GET.get("search")
        query = request.GET.get("search")
        clients = (
            clients.filter(first_name__icontains=query)
            | clients.filter(last_name__icontains=query)
            | clients.filter(email__icontains=query)
            | clients.filter(phone_number__icontains=query)
        )

    if request.method == "POST" and request.htmx:
        data = request.POST
        print(data)
        first_name: str = data.get("first_name", "")
        last_name: str = data.get("last_name", "")
        email: str = data.get("email", "")
        phone_number: str = data.get("phone_number", "")
        delivery_address: str = data.get("address", "")
        context["submitted_f_name"] = first_name
        context["submitted_l_name"] = last_name
        context["submitted_email"] = email
        context["submitted_phone"] = phone_number
        context["submitted_address"] = delivery_address

        errors = sanitize_post_data(data)
        context.update(errors)
        for error in errors.values():
            messages.add_message(request, messages.ERROR, error)

        if len(errors) > 0:
            context["clients"], context["page_range"] = get_paginated_query(
                clients, request
            )
            return render(request, "clients.html", context)
        try:
            client = update_or_create_client(data, None)
            messages.add_message(
                request, messages.SUCCESS, "Client created successfully!"
            )
        except Exception as e:
            print(e)
            messages.add_message(
                request, messages.ERROR, "An error occurred while creating client!"
            )
            context["clients"], context["page_range"] = get_paginated_query(
                clients, request
            )
            return render(request, "clients.html", context)

        context["clients"], context["page_range"] = get_paginated_query(
            Client.objects.all(), request
        )
        response = render(request, "clients.html", context)
        response["HX-Retarget"] = "#clients-container"
        response["HX-Reselect"] = "#clients-container"
        response["HX-Trigger-After-Swap"] = "close-create-form"
        return response

    context["clients"], context["page_range"] = get_paginated_query(clients, request)
    return render(request, "clients.html", context)


def sanitize_post_data(data: dict) -> dict:
    errors: dict = {}
    for key, value in data.items():
        if value is None or value.strip() == "":
            errors[
                f"{key}_error"
            ] = f"{str(key).replace('_', ' ').capitalize()} is required!"
    return errors


def update_or_create_client(data: dict, id: int | None):
    if id is None:
        client = Client.objects.create(
            first_name=data.get("first_name", "").strip(),
            last_name=data.get("last_name", "").strip(),
            email=data.get("email", "").strip(),
            phone_number=data.get("phone_number", "").strip(),
            delivery_address=data.get("address", "").strip(),
        )
    else:
        client = Client.objects.get(pk=id)
        client.first_name = data.get("first_name", "").strip()
        client.last_name = data.get("last_name", "").strip()
        client.email = data.get("email", "").strip()
        client.phone_number = data.get("phone_number", "").strip()
        client.delivery_address = data.get("address", "").strip()
        client.save()
    return client


@login_required
def client_item_view(request, pk):
    client = Client.objects.get(pk=pk)
    context: dict = {
        "client": client,
    }

    if request.htmx and request.method == "DELETE":
        client.delete()
        messages.add_message(request, messages.SUCCESS, "Client deleted successfully!")
        context["clients"], context["page_range"] = get_paginated_query(
            Client.objects.all(), request
        )
        response = render(request, "clients.html", context)
        response["HX-Push-Url"] = resolve_url("clients_view")
        return response

    if request.method == "POST":
        data = request.POST
        print(data)
        errors = sanitize_post_data(data)
        context.update(errors)
        for error in errors.values():
            messages.add_message(request, messages.ERROR, error)
        if len(errors) > 0:
            return render(request, "client_page.html", context)
        try:
            client = update_or_create_client(data, pk)
            messages.add_message(
                request, messages.SUCCESS, "Client updated successfully!"
            )
        except Exception as e:
            print(e)
            messages.add_message(
                request, messages.ERROR, "An error occurred while updating client!"
            )
        context["client"] = client

    return render(request, "client_page.html", context)


@login_required
def orders_view(request):
    context: dict = {}
    user: User = request.user
    context["orders"] = Order.objects.all()
    context["orders_count"] = Order.objects.all().count()
    context["order_statuses"] = Order.OrderStatus.choices

    return render(request, "orders.html", context)



def hx_search_clients(request):
    context: dict = {}
    user: User = request.user
    clients = Client.objects.all()
    if "clients_search" in request.GET and request.GET.get("clients_search").strip() != "":
        context["clients_search"] = request.GET.get("clients_search")
        query = request.GET.get("clients_search")
        clients = (
            clients.filter(first_name__icontains=query)
            | clients.filter(last_name__icontains=query)
            | clients.filter(email__icontains=query)
            | clients.filter(phone_number__icontains=query)
        )
    return render(request, "partials/clientsSearchResults.html", {"clients": clients})
