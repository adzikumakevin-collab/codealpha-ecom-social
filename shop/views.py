from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import OrderCreateForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product_id=product_id)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product_id=product_id)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {
        'cart_items': list(cart),
        'total_price': cart.get_total_price()
    })

@login_required
def checkout(request):
    cart = Cart(request)
    if not list(cart):
        return redirect('product_list')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'shop/order_success.html', {'order': order})
    else:
        form = OrderCreateForm()
        
    return render(request, 'shop/checkout.html', {
        'cart_items': list(cart),
        'total_price': cart.get_total_price(),
        'form': form
    })