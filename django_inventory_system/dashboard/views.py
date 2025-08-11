from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, OrderForm,CreateUserForm
from django.contrib.auth.models import User
from .models import Product, Order,OrderHistory, ProductHistory
from django.http import HttpResponseForbidden
from django.contrib import messages

import xml.etree.ElementTree as ET
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.timezone import now
import os

# Create your views here.

@login_required
def index(request):
    user = request.user
    if user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=user)

    products = Product.objects.filter(quantity__gt=0)
    users = User.objects.all()

    total_users = users.count()
    total_orders = orders.count()

    total_products = products.count()

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        
    }
    return render(request,'dashboard/index.html',context)

@login_required
def product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Make sure to support image uploads
        if form.is_valid():
            name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            image = form.cleaned_data.get('image')

            existing_product = Product.objects.filter(name__iexact=name).first()

            if existing_product:
                # Update existing product
                existing_product.quantity += quantity

                # Update price and description if different
                if existing_product.price != price:
                    existing_product.price = price
                if existing_product.description != description:
                    existing_product.description = description
                if image and existing_product.image != image:
                    existing_product.image = image

                existing_product.save()
                create_product_history(existing_product, movement_type='updated')
                messages.success(request, f"{name} already exists — updated quantity and info.")
            else:
                # Create a new product
                form.save()
                messages.success(request, f"{name} has been added.")

                # Add to history
                create_product_history(form.instance, movement_type='added')

            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/product.html', context)


@login_required
def product_manage(request):
    products = Product.objects.filter(quantity__gt=0)
    context = {
        'products': products,
    }
    return render(request, 'dashboard/product_manage.html', context)

@login_required
def product_update(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if(form.is_valid()):
            form.save()
            # Update the product history
            create_product_history(form.instance, movement_type='updated')
            return redirect('dashboard-product-manage')
    else:
        form =ProductForm(instance = product)

    context = {
        'form':form,
        'product': product,
    }
    return render(request,'dashboard/product_update.html',context)

@login_required
def product_view(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request,'dashboard/product_view.html',context)


# ORDER
@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)   
            order.user = request.user 

            product = order.product
            ordered_qty = order.quantity

            if (product.quantity < ordered_qty):
                # My alert error css is not working so I will use the warning css, I tweaked the css of warning to look like error
                messages.info(request, f'Only {product.quantity} items left in stock for {product.name}.')
                return redirect('dashboard-order')
            
            product.quantity -= ordered_qty
            product.save()
            order.save()
            # CHeck Quantity

           
        
            #Flash messages
            messages.success(request, 'Order has been added')
            
            # Add to history
            create_order_history(form.instance, movement_type='added')
            
            return redirect('dashboard-order')
    else:
        form = OrderForm()
    
    context = {
        'form': form,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def order_manage(request):
    user = request.user
    if user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=user)
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/order_manage.html', context)

@login_required
def order_update(request, pk):
    order = Order.objects.get(id=pk)
    old_quantity = order.quantity
    product = order.product

    if request.method == "POST":
        form = OrderForm(request.POST,instance = order)
        if(form.is_valid()):
            updated_order = form.save(commit=False)

            new_quantity = updated_order.quantity
            product.quantity += old_quantity 

            if(product.quantity < new_quantity):
                messages.info(request, f'Only {product.quantity} items left in stock for {product.name}.')
                return redirect('dashboard-order-manage')
            product.quantity -= new_quantity

            product.save()
            updated_order.save()

            create_order_history(form.instance, movement_type='updated')
            messages.success(request, 'Order has been updated')
            return redirect('dashboard-order-manage')
    else:
        form = OrderForm(instance = order)

    context = {
        'form':form,
    }
    return render(request,'dashboard/order_update.html',context)

# USER
@login_required
def user(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been added')
            return redirect('dashboard-user')
    else:
        form = CreateUserForm()

    context = {
        'form': form,
    }
    return render(request,'dashboard/user.html',context)

@login_required
def user_manage(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboard/user_manage.html', context)

@login_required
def user_view(request, pk):
    user = User.objects.get(id=pk)
    context = {
        'user': user,
    }
    return render(request,'dashboard/user_view.html',context)







# XMLs

def build_xml_from_queryset(queryset, root_name, item_name, fields):
    root = ET.Element(root_name)

    for obj in queryset:
        item = ET.SubElement(root, item_name)
        for field in fields:
            value = getattr(obj, field)
            ET.SubElement(item, field).text = str(value)

    return ET.tostring(root, encoding='utf-8', method='xml')

def save_xml_to_file(xml_data, filename):
    output_path = os.path.join("XML", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(xml_data)

from django.contrib import messages
from django.shortcuts import redirect

def product_xml(request):
    fields = ['id', 'name', 'price', 'quantity', 'description', 'date_added', 'date_updated']
    xml_data = build_xml_from_queryset(Product.objects.all(), "products", "product", fields)
    save_xml_to_file(xml_data, "products.xml")
    
    messages.success(request, "Product XML export complete!")
    return redirect('dashboard-product-manage')  # or wherever you want to redirect

def order_xml(request):
    fields = ['id', 'customer_name', 'user_id', 'product_id', 'quantity', 'order_date', 'order_notes']
    xml_data = build_xml_from_queryset(Order.objects.all(), "orders", "order", fields)
    save_xml_to_file(xml_data, "orders.xml")
    
    messages.success(request, "Order XML export complete!")
    return redirect('dashboard-order-manage')

def order_history_xml(request):
    fields = ['id', 'user', 'customer_name', 'product_name', 'quantity', 'price_per_item',
              'total_price', 'order_notes', 'timestamp', 'movement_type']
    xml_data = build_xml_from_queryset(OrderHistory.objects.all(), "order_history", "entry", fields)
    save_xml_to_file(xml_data, "order_history.xml")
    
    messages.success(request, "Order History XML export complete!")
    return redirect('dashboard-order-history')

def product_history_xml(request):
    fields = ['id', 'name', 'price', 'quantity', 'date_added', 'movement_type']
    xml_data = build_xml_from_queryset(ProductHistory.objects.all(), "product_history", "entry", fields)
    save_xml_to_file(xml_data, "product_history.xml")
    
    messages.success(request, "Product History XML export complete!")
    return redirect('dashboard-product-history')

def user_xml(request):
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_staff',
              'is_active', 'is_superuser', 'last_login', 'date_joined']
    xml_data = build_xml_from_queryset(User.objects.all(), "users", "user", fields)
    save_xml_to_file(xml_data, "users.xml")
    
    messages.success(request, "User XML export complete!")
    return redirect('dashboard-user-manage')




# DELETE

@login_required
def delete(request, model_name, pk):
    model = None
    if model_name == 'product':
        model = Product
    elif model_name == 'order':
        model = Order
    elif model_name == 'user':
        model = User
    else:
        return HttpResponseForbidden("Invalid model")

    instance = get_object_or_404(model, id=pk)

    if request.method == 'POST':
        if model_name == 'order':
            # Only restore product quantity if not staff
            if not request.user.is_staff:
                product = instance.product
                product.quantity += instance.quantity
                product.save()
            create_order_history(instance, movement_type='purchased')
        
        elif model_name == 'product':
            create_product_history(instance, movement_type='deleted')
        instance.delete()
            
        if model_name == 'product':
            return redirect('dashboard-product-manage')
        elif model_name == 'order':
            return redirect('dashboard-order-manage')
        elif model_name == 'user':
            return redirect('dashboard-user-manage')

    context = {
        'object': instance,
        'model_name': model_name
    }
    return render(request, 'dashboard/delete.html', context)


# History
def order_history(request):
    sort = request.GET.get('sort', 'timestamp')
    order = request.GET.get('order', 'desc')

    allowed_sorts = ['customer_name', 'product_name', 'quantity', 'price_per_item', 'total_price', 'user__username', 'timestamp', 'movement_type']
    if sort not in allowed_sorts:
        sort = 'timestamp'

    ordering = sort if order == 'asc' else f'-{sort}'

    history_entries = OrderHistory.objects.all().order_by(ordering)

    for entry in history_entries:
        entry.formatted_date = entry.timestamp.strftime('%B %d %Y')  # Format "May 18 2025"

    context = {
        'history_entries': history_entries,
        'current_sort': sort,
        'current_order': order
    }

    return render(request, 'dashboard/order_history.html', context)



def product_history(request):
    sort = request.GET.get('sort', 'date_added')
    order = request.GET.get('order', 'desc')

    # Protect against invalid fields
    allowed_sorts = ['name', 'price', 'quantity', 'date_added', 'movement_type']
    if sort not in allowed_sorts:
        sort = 'date_added'

    ordering = sort if order == 'asc' else f'-{sort}'

    history_entries = ProductHistory.objects.all().order_by(ordering)

    for entry in history_entries:
        entry.formatted_date = entry.date_added.strftime('%B %d %Y')  #

    context = {
        'history_entries': history_entries,
        'current_sort': sort,
        'current_order': order
    }
    return render(request, 'dashboard/product_history.html', context)



# Create a product history entry
def create_product_history(product, movement_type):
    ProductHistory.objects.create(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        date_added=now(),
        movement_type=movement_type
    )

def create_order_history(order, movement_type):
    OrderHistory.objects.create(
        user = order.user.username,
        customer_name=order.customer_name,
        product_name=order.product.name,
        quantity=order.quantity,
        price_per_item=order.product.price,
        total_price=order.total_price(),
        order_notes=order.order_notes,
        movement_type=movement_type,
        timestamp=order.order_date,
    )


# Sorting

    