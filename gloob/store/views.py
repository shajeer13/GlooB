from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid username or password'})
    return render(request, 'store/login.html')

# Signup view
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')

        if password != confirm_password:
            context = {'error': "Passwords do not match!"}
            return render(request, 'store/signup.html', context)

        if User.objects.filter(username=username).exists():
            context = {'error': "Username already taken!"}
            return render(request, 'store/signup.html', context)

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'store/signup.html')

# Home view
@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# Cart views
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
