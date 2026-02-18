# store/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('home')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'store/login.html', context)
    else:
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
        
        # Create new user
        User.objects.create_user(username=username, password=password)
        messages.success(request, f"Account created for {username}! Please login.")
        return redirect('login')
    
    return render(request, 'store/signup.html')


# Home view
def home(request):
    return render(request, 'store/home.html')


# Cart view
def cart(request):
    return render(request, 'store/cart.html')
# store/views.py
from django.shortcuts import render, redirect

# Existing views: home, login_view, signup, cart

def add_to_cart(request, id):
    # നിങ്ങൾ products DB അല്ലെങ്കിൽ session/cart logic use ചെയ്യാം
    # simplified version:
    context = {'message': f'Product {id} added to cart!'}
    return render(request, 'store/cart.html', context)


