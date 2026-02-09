from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('cart/', views.cart, name='cart'),  # ഇങ്ങനെ ഉണ്ടെങ്കിൽ
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
]
