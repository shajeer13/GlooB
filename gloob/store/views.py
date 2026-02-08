from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from .models import Product

@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    products_in_cart = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        product.quantity = quantity
        product.total_price = product.price * quantity
        total += product.total_price
        products_in_cart.append(product)
    return render(request, 'store/cart.html', {
        'products_in_cart': products_in_cart,
        'total': total
    })

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1
    request.session['cart'] = cart
    return redirect('cart')
