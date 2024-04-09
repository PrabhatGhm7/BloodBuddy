from django.contrib import admin
from django.urls import path
from . import views
from django.urls import reverse

urlpatterns = [
    path('home/', views.home,name='home'),
    path('signup/', views.signup,name='signup'),
    path('signin/', views.signin,name='signin'),
    path('profile/', views.profile,name='profile'),
    path('signout/', views.signout,name='logout'),
    path('search/', views.search,name='search'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    
]
    