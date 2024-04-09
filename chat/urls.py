from django.urls import path
from . import views
app_name = 'chat'
urlpatterns = [
    path('chat/', views.chathome, name='chathome'),
    path('<str:room>/', views.room, name='room'),
    path('chat/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]