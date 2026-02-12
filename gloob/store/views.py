from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
        
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    
    return render(request, 'store/signup.html')


# Home view
def home(request):
    return render(request, 'store/home.html')
